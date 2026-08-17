from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from .models import Usuario
from .suap import oauth


def login(request):
    redirect_uri = request.build_absolute_uri("/usuarios/callback/")
    return oauth.suap.authorize_redirect(request, redirect_uri)


def callback(request):
    token = oauth.suap.authorize_access_token(request)

    request.session["suap_token"] = token

    resposta = oauth.suap.get("rh/meus-dados",token=token)

    resposta.raise_for_status()

    dados = resposta.json()

    id_suap = dados["id"]
    nome = dados["nome_usual"]
    email = dados["email"]
    matricula = dados["matricula"]
    tipo_usuario = dados["tipo_vinculo"]

    vinculo = dados["vinculo"]
    
    campus = vinculo.get("campus", "")
    categoria = ""
    curso = ""

    if tipo_usuario == "Aluno":
        detalhamento = vinculo.get("detalhamento", {})
        curso = detalhamento.get("curso", "")

    elif tipo_usuario == "Servidor":
        detalhamento = vinculo.get("detalhamento", {})
        categoria = detalhamento.get("categoria", "")

    usuario, criado = Usuario.objects.update_or_create(
        id_suap=id_suap,
        defaults={
            "nome": nome,
            "email": email,
            "matricula": matricula,
            "tipo_usuario": tipo_usuario,
            "categoria": categoria,
            "campus": campus,
            "curso": curso,
            "foto": dados.get("url_foto_150x200", ""),
        }
    )
    

    return redirect("/")


def logout(request):
    request.session.pop("suap_token", None)
    django_logout(request)

    return redirect("/")

