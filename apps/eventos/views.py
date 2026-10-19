from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from apps.usuarios.models import Usuario
from .forms import EventoForm
from .models import Evento
from django.db.models import Q
from apps.materias.models import AtividadeClassroom


def _eh_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _dados_evento(evento):
    return {
        "id": str(evento.id),
        "title": evento.titulo,
        "start": f"{evento.data.isoformat()}T{evento.horario.strftime('%H:%M:%S')}",
        "data_display": evento.data.strftime("%d/%m/%Y"),
        "horario_display": evento.horario.strftime("%H:%M"),
        "descricao": evento.descricao,
        "categoria": evento.categoria,
        "categoria_label": evento.get_categoria_display(),
        "visibilidade": evento.visibilidade,
        "visibilidade_label": evento.get_visibilidade_display(),
        "turma": evento.turma or "",
        "criador_id": str(evento.criador_id),
        "edit_url": reverse("eventos:editar_evento", args=[evento.id]),
        "delete_url": reverse("eventos:excluir_evento", args=[evento.id]),
        "can_edit": True,
    }

# CRUD EVENTOS

def criar_evento(request):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        if _eh_ajax(request):
            return JsonResponse({"ok": False, "error": "Sua sessão expirou. Entre novamente."}, status=401)
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == "POST":
        form = EventoForm(request.POST)

        if form.is_valid():
            evento = form.save(commit=False)

            evento.criador = usuario

            evento.save()

            if _eh_ajax(request):
                return JsonResponse({"ok": True, "event": _dados_evento(evento)})

            return redirect("eventos:listar_eventos")
        if _eh_ajax(request):
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

    else:
        form = EventoForm()

    return render(request, "eventos/criar_evento.html" ,{"form": form, "usuario": usuario})

def lista_eventos(request):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    eventos = Evento.objects.filter(
        Q(visibilidade="PESSOAL", criador=usuario)
        |
        Q(visibilidade="TURMA", turma=usuario.turma)
        |
        Q(visibilidade="TODOS")
    ).order_by("data", "horario")


    return render(request, "eventos/listar_eventos.html", {
        "eventos": eventos,
        "usuario": usuario,
        "event_form": EventoForm(),
    })

def editar_evento(request, id):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        if _eh_ajax(request):
            return JsonResponse({"ok": False, "error": "Sua sessão expirou. Entre novamente."}, status=401)
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    evento = get_object_or_404(Evento, id=id)
    if evento.criador.id != usuario.id:
        if _eh_ajax(request):
            return JsonResponse({"ok": False, "error": "Você não tem permissão para editar este evento."}, status=403)
        return redirect("eventos:listar_eventos")

    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)

        if form.is_valid():
            evento = form.save()

            if _eh_ajax(request):
                return JsonResponse({"ok": True, "event": _dados_evento(evento)})

            return redirect("eventos:listar_eventos")
        if _eh_ajax(request):
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

    else:
        form = EventoForm(instance=evento)

    return render(request, "eventos/editar_evento.html", {
            "form": form,
            "evento": evento,
            "usuario": usuario,
        }
    )

def excluir_evento(request, id):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    evento = Evento.objects.get(id=id)

    if evento.criador.id != usuario.id:
        return redirect("eventos:listar_eventos")

    if request.method == "POST":
        evento.delete()

        return redirect("eventos:listar_eventos")

    return render(request, "eventos/excluir_evento.html", {"evento": evento, "usuario": usuario})

# FIM CRUD EVENTOS -----------------------------------------------------------------------------

def calendario(request):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    eventos = Evento.objects.filter(
        Q(visibilidade="PESSOAL", criador=usuario)
        |
        Q(visibilidade="TURMA", turma=usuario.turma)
        |
        Q(visibilidade="TODOS")
    ).order_by("data", "horario")

    atividades_classroom = AtividadeClassroom.objects.filter(usuario=usuario).order_by("data_entrega")

    calendar_events = []
    for evento in eventos:
        event_data = _dados_evento(evento)
        event_data["can_edit"] = evento.criador_id == usuario.id
        event_data["backgroundColor"] = _cor_categoria(evento.categoria)
        event_data["borderColor"] = _cor_categoria(evento.categoria)
        calendar_events.append(event_data)

    for atividade in atividades_classroom:
        if not atividade.data_entrega:
            continue
        data_entrega = atividade.data_entrega
        if timezone.is_naive(data_entrega):
            data_entrega = timezone.make_aware(data_entrega, timezone.get_default_timezone())
        data_entrega = timezone.localtime(data_entrega)
        calendar_events.append({
            "id": f"classroom-{atividade.id}",
            "title": atividade.titulo,
            "start": data_entrega.isoformat(),
            "descricao": "Atividade do Google Classroom",
            "categoria": "CLASSROOM",
            "categoria_label": "Google Classroom",
            "origem": "classroom",
            "link": atividade.link,
            "backgroundColor": "#2563eb",
            "borderColor": "#2563eb",
            "can_edit": False,
        })

    return render(request, "eventos/calendario.html", {
        "usuario": usuario,
        "usuario_id": str(usuario.id),
        "calendar_events": calendar_events,
        "event_form": EventoForm(),
        "create_event_url": reverse("eventos:criar_evento"),
    })


def _cor_categoria(categoria):
    return {
        "PROVA": "#dc2626",
        "TRABALHO": "#ea580c",
        "ATIVIDADE": "#2563eb",
        "ESTUDO": "#7c3aed",
        "PESSOAL": "#0f9488",
        "OUTRO": "#64748b",
    }.get(categoria, "#64748b")
