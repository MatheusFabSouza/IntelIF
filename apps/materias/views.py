from django.shortcuts import render, redirect

from apps.usuarios.models import Usuario
from .models import Materia
from .utils import obter_proxima_aula


def lista_materias(request):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("/usuarios/login/")

    usuario = Usuario.objects.get(id=usuario_id)

    materias = Materia.objects.filter(
        usuario=usuario).prefetch_related("professores", "horarios")

    for materia in materias:
        materia.proxima_aula = obter_proxima_aula(materia)

    return render(request, "materias/lista_materias.html", {"materias": materias})

def detalhes_materia(request, id):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("/usuarios/login/")

    usuario = Usuario.objects.get(id=usuario_id)

    materia = Materia.objects.prefetch_related(
        "professores",
        "horarios"
    ).get(
        id=id,
        usuario=usuario
    )

    materia.proxima_aula = obter_proxima_aula(materia)

    return render(request, "materias/detalhes_materia.html", {"materia": materia})
