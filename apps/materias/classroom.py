from datetime import datetime, timedelta, timezone as datetime_timezone

from django.utils import timezone

from apps.materias.models import AtividadeClassroom
from apps.usuarios.google import obter_turmas, obter_atividades


def sincronizar_atividades_classroom(usuario, token, completa=False):

    limite_passado = timezone.now() - timedelta(days=30)

    turmas = obter_turmas(token)

    atividades_salvas = 0

    for turma in turmas.get("courses", []):

        curso_id = turma.get("id")
        curso_nome = turma.get("name", "")

        if not curso_id:
            continue

        atividades = obter_atividades(
            token,
            curso_id
        )

        for atividade in atividades.get("courseWork", []):

            due_date = atividade.get("dueDate")

            # Sem data de entrega não entra no calendário
            if not due_date:
                continue

            ano = due_date["year"]
            mes = due_date["month"]
            dia = due_date["day"]

            due_time = atividade.get("dueTime", {})

            if due_time:
                # O Google Classroom entrega dueDate/dueTime em UTC.
                data_utc = datetime(
                    ano,
                    mes,
                    dia,
                    due_time.get("hours", 0),
                    due_time.get("minutes", 0),
                    due_time.get("seconds", 0),
                    tzinfo=datetime_timezone.utc,
                )
                data_entrega = timezone.localtime(data_utc)
            else:
                # Sem horário definido no Classroom, representa o fim do dia local.
                data_entrega = datetime(
                    ano,
                    mes,
                    dia,
                    23,
                    59,
                    0,
                    tzinfo=timezone.get_default_timezone(),
                )

            # Na sincronização rápida, ignora atividades com mais de 30 dias.
            if not completa and data_entrega < limite_passado:
                continue

            id_classroom = atividade.get("id")

            if not id_classroom:
                continue

            AtividadeClassroom.objects.update_or_create(
                id_classroom=id_classroom,
                usuario=usuario,
                defaults={
                    "titulo": atividade.get(
                        "title",
                        "Atividade"
                    ),
                    "data_entrega": data_entrega,
                    "link": atividade.get(
                        "alternateLink",
                        ""
                    ),
                    "curso_classroom_id": curso_id,
                    "curso_nome": curso_nome,
                }
            )

            atividades_salvas += 1

    return atividades_salvas
