import mimetypes

from django.db.models import Prefetch, Q
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date

from apps.usuarios.models import Usuario
from .forms import ConteudoMateriaForm, MateriaPersonalizacaoForm, TopicoForm
from .models import ConteudoMateria, Materia, Topico
from .utils import obter_proxima_aula


def _usuario_da_sessao(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return None
    return Usuario.objects.filter(id=usuario_id).first()


def lista_materias(request):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return redirect("/usuarios/login/")

    materias = Materia.objects.filter(usuario=usuario).prefetch_related("professores", "horarios")
    for materia in materias:
        materia.proxima_aula = obter_proxima_aula(materia)

    return render(request, "materias/lista_materias.html", {"materias": materias, "usuario": usuario})


def detalhes_materia(request, id):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return redirect("/usuarios/login/")

    materia = get_object_or_404(
        Materia.objects.prefetch_related("professores", "horarios"),
        id=id,
        usuario=usuario,
    )

    if request.method == "POST" and "status" in request.POST:
        novo_status = request.POST.get("status")
        if novo_status in dict(Materia.STATUS_CHOICES):
            materia.status = novo_status
            materia.save(update_fields=["status"])
            return redirect("materias:detalhes_materia", id=materia.id)

    filtros = {
        "q": request.GET.get("q", "").strip(),
        "tipo": request.GET.get("tipo", "").strip(),
        "data": request.GET.get("data", "").strip(),
        "periodo": request.GET.get("periodo", "").strip(),
    }
    conteudos = ConteudoMateria.objects.all()
    if filtros["tipo"] in dict(ConteudoMateria.TIPOS):
        conteudos = conteudos.filter(tipo=filtros["tipo"])
    data_filtro = parse_date(filtros["data"]) if filtros["data"] else None
    if data_filtro:
        conteudos = conteudos.filter(adicionado_em__date=data_filtro)
    if filtros["periodo"]:
        conteudos = conteudos.filter(periodo__iexact=filtros["periodo"])
    if filtros["q"]:
        termo = filtros["q"]
        conteudos = conteudos.filter(
            Q(titulo__icontains=termo)
            | Q(anotacao__icontains=termo)
            | Q(link__icontains=termo)
            | Q(arquivo__icontains=termo)
            | Q(topico__titulo__icontains=termo)
        )

    filtros_ativos = bool(filtros["q"] or filtros["tipo"] or data_filtro or filtros["periodo"])
    topicos = Topico.objects.filter(materia=materia)
    if filtros_ativos:
        topicos = topicos.filter(conteudos__in=conteudos).distinct()
    topicos = topicos.prefetch_related(Prefetch("conteudos", queryset=conteudos.order_by("-adicionado_em")))

    materia.proxima_aula = obter_proxima_aula(materia)
    return render(request, "materias/detalhes_materia.html", {
        "materia": materia,
        "usuario": usuario,
        "status_choices": Materia.STATUS_CHOICES,
        "tipo_choices": ConteudoMateria.TIPOS,
        "periodo_choices": ConteudoMateria.objects.filter(
            topico__materia=materia
        ).exclude(periodo="").values_list("periodo", flat=True).distinct().order_by("periodo"),
        "topicos": topicos,
        "filtros": filtros,
        "filtros_ativos": filtros_ativos,
        "icone_choices": Materia.ICONE_CHOICES,
        "materia_color_choices": [
            {"value": "#A78BFA", "label": "Roxo"},
            {"value": "#3B82F6", "label": "Azul"},
            {"value": "#F97316", "label": "Laranja"},
            {"value": "#EC4899", "label": "Rosa"},
            {"value": "#DC2626", "label": "Vermelho"},
        ],
    })


def editar_materia(request, materia_id):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return JsonResponse({"ok": False, "errors": {"auth": [{"message": "Sua sessão expirou. Entre novamente."}]}}, status=401)
    materia = get_object_or_404(Materia, id=materia_id, usuario=usuario)
    if request.method != "POST":
        return JsonResponse({"ok": False, "errors": {"method": [{"message": "Método inválido."}]}}, status=405)

    form = MateriaPersonalizacaoForm(request.POST, request.FILES, instance=materia)
    if form.is_valid():
        materia = form.save()
        return JsonResponse({
            "ok": True,
            "cor": materia.cor,
            "icone": materia.icone_css_class,
            "icone_imagem_url": materia.icone_imagem.url if materia.icone_imagem else "",
            "descricao_pessoal": materia.descricao_pessoal,
        })

    return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)


def criar_topico(request, materia_id):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return redirect("/usuarios/login/")
    materia = get_object_or_404(Materia, id=materia_id, usuario=usuario)

    form = TopicoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        topico = form.save(commit=False)
        topico.materia = materia
        topico.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string("materias/partials/topico_card.html", {
                "topico": topico,
                "materia": materia,
            }, request=request)
            return JsonResponse({"ok": True, "html": html})
        return redirect("materias:detalhes_materia", id=materia.id)

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

    return render(request, "materias/topico_form.html", {
        "form": form, "materia": materia, "usuario": usuario, "titulo_pagina": "Novo tópico",
    })


def editar_topico(request, materia_id, topico_id):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return redirect("/usuarios/login/")
    materia = get_object_or_404(Materia, id=materia_id, usuario=usuario)
    topico = get_object_or_404(Topico, id=topico_id, materia=materia)

    form = TopicoForm(request.POST or None, instance=topico)
    if request.method == "POST" and form.is_valid():
        topico = form.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string("materias/partials/topico_card.html", {
                "topico": topico,
                "materia": materia,
            }, request=request)
            return JsonResponse({"ok": True, "html": html})
        return redirect("materias:detalhes_materia", id=materia.id)

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

    return render(request, "materias/topico_form.html", {
        "form": form, "materia": materia, "topico": topico, "usuario": usuario, "titulo_pagina": "Editar tópico",
    })


def excluir_topico(request, materia_id, topico_id):
    requisicao_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    usuario = _usuario_da_sessao(request)
    if not usuario:
        if requisicao_ajax:
            return JsonResponse({"ok": False, "error": "Sua sessão expirou. Entre novamente."}, status=401)
        return redirect("/usuarios/login/")
    try:
        materia = get_object_or_404(Materia, id=materia_id, usuario=usuario)
        topico = get_object_or_404(Topico, id=topico_id, materia=materia)
    except Http404:
        if requisicao_ajax:
            return JsonResponse({"ok": False, "error": "Este tópico já foi excluído ou não foi encontrado."}, status=404)
        raise

    if request.method == "POST":
        for conteudo in topico.conteudos.all():
            if conteudo.arquivo:
                conteudo.arquivo.delete(save=False)
        topico.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "kind": "topico", "id": str(topico_id)})
        return redirect("materias:detalhes_materia", id=materia.id)

    return render(request, "materias/confirmar_exclusao.html", {
        "objeto": topico, "tipo_objeto": "tópico", "materia": materia, "usuario": usuario,
    })


def criar_conteudo(request, materia_id, topico_id):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return redirect("/usuarios/login/")
    materia = get_object_or_404(Materia, id=materia_id, usuario=usuario)
    topico = get_object_or_404(Topico, id=topico_id, materia=materia)

    form = ConteudoMateriaForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        conteudo = form.save(commit=False)
        conteudo.topico = topico
        conteudo.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string("materias/partials/conteudo_row.html", {
                "conteudo": conteudo,
                "materia": materia,
            }, request=request)
            return JsonResponse({"ok": True, "html": html})
        return redirect("materias:detalhes_materia", id=materia.id)

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

    return render(request, "materias/conteudo_form.html", {
        "form": form, "materia": materia, "topico": topico, "usuario": usuario, "titulo_pagina": "Adicionar conteúdo",
    })


def editar_conteudo(request, materia_id, conteudo_id):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return redirect("/usuarios/login/")
    materia = get_object_or_404(Materia, id=materia_id, usuario=usuario)
    conteudo = get_object_or_404(ConteudoMateria, id=conteudo_id, topico__materia=materia)

    form = ConteudoMateriaForm(request.POST or None, request.FILES or None, instance=conteudo)
    if request.method == "POST" and form.is_valid():
        conteudo = form.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string("materias/partials/conteudo_row.html", {
                "conteudo": conteudo,
                "materia": materia,
            }, request=request)
            return JsonResponse({"ok": True, "html": html})
        return redirect("materias:detalhes_materia", id=materia.id)

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)

    return render(request, "materias/conteudo_form.html", {
        "form": form, "materia": materia, "topico": conteudo.topico, "conteudo": conteudo,
        "usuario": usuario, "titulo_pagina": "Editar conteúdo",
    })


def excluir_conteudo(request, materia_id, conteudo_id):
    requisicao_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    usuario = _usuario_da_sessao(request)
    if not usuario:
        if requisicao_ajax:
            return JsonResponse({"ok": False, "error": "Sua sessão expirou. Entre novamente."}, status=401)
        return redirect("/usuarios/login/")
    try:
        materia = get_object_or_404(Materia, id=materia_id, usuario=usuario)
        conteudo = get_object_or_404(ConteudoMateria, id=conteudo_id, topico__materia=materia)
    except Http404:
        if requisicao_ajax:
            return JsonResponse({"ok": False, "error": "Este conteúdo já foi excluído ou não foi encontrado."}, status=404)
        raise

    if request.method == "POST":
        if conteudo.arquivo:
            conteudo.arquivo.delete(save=False)
        conteudo.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "kind": "conteudo", "id": str(conteudo_id)})
        return redirect("materias:detalhes_materia", id=materia.id)

    return render(request, "materias/confirmar_exclusao.html", {
        "objeto": conteudo, "tipo_objeto": "conteúdo", "materia": materia, "usuario": usuario,
    })


def baixar_conteudo(request, conteudo_id):
    usuario = _usuario_da_sessao(request)
    if not usuario:
        return redirect("/usuarios/login/")
    conteudo = get_object_or_404(
        ConteudoMateria,
        id=conteudo_id,
        topico__materia__usuario=usuario,
        tipo=ConteudoMateria.TIPO_ARQUIVO,
    )
    if not conteudo.arquivo:
        raise Http404("Arquivo não encontrado.")
    try:
        arquivo = conteudo.arquivo.open("rb")
    except (FileNotFoundError, OSError):
        raise Http404("Arquivo não encontrado.")
    filename = conteudo.arquivo.name.rsplit("/", 1)[-1]
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    return FileResponse(arquivo, as_attachment=False, filename=filename, content_type=content_type)
