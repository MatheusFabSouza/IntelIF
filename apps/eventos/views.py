from django.shortcuts import render, redirect
from apps.usuarios.models import Usuario
from .forms import EventoForm
from .models import Evento
from django.db.models import Q
from apps.materias.models import AtividadeClassroom

# CRUD EVENTOS

def criar_evento(request):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == "POST":
        form = EventoForm(request.POST)

        if form.is_valid():
            evento = form.save(commit=False)

            evento.criador = usuario

            evento.save()

            return redirect("eventos:listar_eventos")

    else:
        form = EventoForm()

    return render(request, "eventos/criar_evento.html" ,{"form": form})

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


    return render(request, "eventos/listar_eventos.html", {"eventos": eventos})

def editar_evento(request, id):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    evento = Evento.objects.get(id=id)
    if evento.criador.id != usuario.id:
        return redirect("eventos:listar_eventos")

    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)

        if form.is_valid():
            form.save()

            return redirect("eventos:listar_eventos")

    else:
        form = EventoForm(instance=evento)

    return render(request, "eventos/editar_evento.html", {
            "form": form,
            "evento": evento,
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

    return render(request, "eventos/excluir_evento.html", {"evento": evento})

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

    return render(request, "eventos/calendario.html", {"eventos": eventos, "usuario_id": str(usuario.id), "atividades_classroom": atividades_classroom})