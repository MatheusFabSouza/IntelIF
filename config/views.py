from datetime import datetime, time, timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from apps.eventos.models import Evento
from apps.materias.models import AtividadeClassroom, Materia
from apps.materias.utils import obter_proxima_aula
from apps.usuarios.models import Usuario


DIAS_CURTOS = {
    0: "SEG",
    1: "TER",
    2: "QUA",
    3: "QUI",
    4: "SEX",
    5: "SÁB",
    6: "DOM",
}


def _usuario_da_sessao(request):
    """
    Retorna o usuário associado à sessão atual.

    Caso a sessão contenha um usuário inválido ou removido,
    limpa os dados de autenticação armazenados.
    """

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return None

    try:
        return Usuario.objects.get(id=usuario_id)

    except (Usuario.DoesNotExist, ValueError, TypeError):
        request.session.pop("usuario_id", None)
        request.session.pop("suap_token", None)
        request.session.pop("google_token", None)

        return None


def _data_local(data_hora):
    """
    Retorna a data local de um DateTimeField.

    Funciona tanto com datetime aware quanto naive.
    """

    if not data_hora:
        return None

    if timezone.is_aware(data_hora):
        data_hora = timezone.localtime(data_hora)

    return data_hora.date()


def _datetime_evento(evento):
    """
    Converte a data e o horário de um Evento em datetime
    compatível com o timezone configurado no Django.
    """

    horario = evento.horario or time.min

    data_hora = datetime.combine(
        evento.data,
        horario,
    )

    if timezone.is_naive(data_hora):
        data_hora = timezone.make_aware(
            data_hora,
            timezone.get_current_timezone(),
        )

    return data_hora


def home(request):
    """
    Página inicial do IntelIF.

    Visitante:
        /
        -> visitante.html

    Usuário autenticado:
        /
        -> home.html
    """

    usuario = _usuario_da_sessao(request)

    # ------------------------------
    # USUÁRIO NÃO AUTENTICADO
    # ------------------------------

    if not usuario:
        return render(
            request,
            "visitante.html",
        )

    # ------------------------------
    # DATAS
    # ------------------------------

    agora = timezone.localtime()

    hoje = agora.date()

    fim_semana = hoje + timedelta(days=6)

    limite_eventos = hoje + timedelta(days=30)

    # ------------------------------
    # MATÉRIAS
    # ------------------------------

    materias = list(
        Materia.objects
        .filter(usuario=usuario)
        .prefetch_related(
            "professores",
            "horarios",
        )
        .order_by("descricao")
    )

    for materia in materias:
        materia.proxima_aula = obter_proxima_aula(
            materia
        )

    # ------------------------------
    # EVENTOS
    # ------------------------------

    filtro_eventos = (
        Q(
            visibilidade="PESSOAL",
            criador=usuario,
        )
        |
        Q(
            visibilidade="TODOS",
        )
    )

    # Eventos da turma só devem entrar caso
    # o usuário possua turma cadastrada.
    if getattr(usuario, "turma", None):
        filtro_eventos |= Q(
            visibilidade="TURMA",
            turma=usuario.turma,
        )

    eventos_qs = (
        Evento.objects
        .filter(filtro_eventos)
        .filter(data__gte=hoje)
        .select_related("criador")
        .order_by(
            "data",
            "horario",
        )
    )

    # ------------------------------
    # GOOGLE CLASSROOM
    # ------------------------------

    atividades_qs = (
        AtividadeClassroom.objects
        .filter(
            usuario=usuario,
            data_entrega__gte=agora,
        )
        .order_by("data_entrega")
    )

    # ------------------------------
    # CALENDÁRIO DOS PRÓXIMOS 7 DIAS
    # ------------------------------

    eventos_semana = list(
        eventos_qs.filter(
            data__lte=fim_semana
        )
    )

    atividades_semana = list(
        atividades_qs.filter(
            data_entrega__date__lte=fim_semana
        )
    )

    dias = []

    for deslocamento in range(7):

        data = hoje + timedelta(
            days=deslocamento
        )

        itens = []

        # Eventos IntelIF
        for evento in eventos_semana:

            if evento.data != data:
                continue

            classe = (
                "orange"
                if evento.categoria in {
                    "PROVA",
                    "TRABALHO",
                }
                else "green"
            )

            itens.append({
                "titulo": evento.titulo,
                "tipo": "evento",
                "classe": classe,
            })

        # Atividades Google Classroom
        for atividade in atividades_semana:

            data_entrega = _data_local(
                atividade.data_entrega
            )

            if data_entrega != data:
                continue

            itens.append({
                "titulo": atividade.titulo,
                "tipo": "classroom",
                "classe": "blue",
            })

        dias.append({
            "data": data,
            "dia_semana": DIAS_CURTOS[
                data.weekday()
            ],
            "numero": data.day,
            "is_today": data == hoje,
            "itens": itens[:2],
            "tem_mais": len(itens) > 2,
        })

    # ------------------------------
    # PRÓXIMAS ATIVIDADES
    # ------------------------------

    proximas = []

    # Classroom
    for atividade in atividades_qs[:6]:

        data_entrega = atividade.data_entrega

        if timezone.is_aware(data_entrega):
            data_entrega = timezone.localtime(
                data_entrega
            )

        proximas.append({
            "titulo": atividade.titulo,
            "subtitulo": (
                atividade.curso_nome
                or "Google Classroom"
            ),
            "quando": data_entrega,
            "origem": "Classroom",
            "link": atividade.link or "",
            "classe": "blue",
        })

    # Eventos IntelIF
    for evento in eventos_qs[:6]:

        classe = (
            "orange"
            if evento.categoria in {
                "PROVA",
                "TRABALHO",
            }
            else "green"
        )

        proximas.append({
            "titulo": evento.titulo,
            "subtitulo": (
                evento.get_categoria_display()
            ),
            "quando": _datetime_evento(
                evento
            ),
            "origem": "IntelIF",
            "link": "",
            "classe": classe,
        })

    # Mistura Classroom + IntelIF
    # e ordena cronologicamente.
    proximas.sort(
        key=lambda item: item["quando"]
    )

    proximas = proximas[:5]

    # ------------------------------
    # CONTADORES
    # ------------------------------

    total_pendentes = atividades_qs.count()

    total_eventos = eventos_qs.filter(
        data__lte=limite_eventos
    ).count()

    total_materias = len(materias)

    classroom_conectado = bool(
        request.session.get("google_token")
    )

    # ------------------------------
    # TEMPLATE
    # ------------------------------

    contexto = {
        "usuario": usuario,

        "materias": materias[:5],
        "total_materias": total_materias,

        "dias": dias,

        "proximas_atividades": proximas,

        "total_pendentes": total_pendentes,
        "total_eventos": total_eventos,

        "classroom_conectado": (
            classroom_conectado
        ),
    }

    return render(
        request,
        "home.html",
        contexto,
    )