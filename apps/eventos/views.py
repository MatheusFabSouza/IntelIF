from django.shortcuts import render, redirect
from apps.usuarios.models import Usuario
from .forms import EventoForm
from .models import Evento

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

    eventos = Evento.objects.all()

    return render(request, "eventos/listar_eventos.html", {"eventos": eventos})

def editar_evento(request, id):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("usuarios:login")

    usuario = Usuario.objects.get(id=usuario_id)

    evento = Evento.objects.get(id=id)

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

    evento = Evento.objects.get(id=id)

    if request.method == "POST":
        evento.delete()

        return redirect("eventos:listar_eventos")

    return render(request, "eventos/excluir_evento.html", {"evento": evento})