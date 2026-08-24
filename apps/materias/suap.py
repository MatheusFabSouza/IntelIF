from datetime import datetime
from apps.materias.models import Materia, Professor, HorarioMateria
from apps.usuarios.suap import obter_diarios

def sincronizar_materias(usuario, token):
    dados = obter_diarios(token)

    diarios = dados.get("results", [])

    for diario in diarios:

        disciplina = diario.get("disciplina", {})

        descricao = disciplina.get("descricao", "")

        if not descricao:
            continue

        materia, criada = Materia.objects.update_or_create(
            id_suap=diario["id"],
            usuario=usuario,
            defaults={
                "descricao": descricao,
            }
        )

        # Professores
        materia.professores.clear()

        for dados_professor in diario.get("professores", []):

            professor, criado = Professor.objects.update_or_create(
                id_suap=dados_professor["id"],
                defaults={
                    "nome": dados_professor["nome"]
                }
            )

            materia.professores.add(professor)

        # Horários
        materia.horarios.all().delete()

        for horario in diario.get("horarios", []):

            horario_texto = horario.get("horario", "")

            if not horario_texto:
                continue

            partes = horario_texto.split(" - ")

            if len(partes) != 2:
                continue

            hora_inicio = datetime.strptime(
                partes[0],
                "%H:%M"
            ).time()

            hora_fim = datetime.strptime(
                partes[1],
                "%H:%M"
            ).time()

            HorarioMateria.objects.create(
                materia=materia,
                dia=horario["dia"],
                hora_inicio=hora_inicio,
                hora_fim=hora_fim
            )
