from django.urls import path
from . import views


app_name = "materias"

urlpatterns = [
    path("", views.lista_materias, name="listar_materias"),
    path("<uuid:id>/", views.detalhes_materia, name="detalhes_materia"),
    path("<uuid:materia_id>/editar/", views.editar_materia, name="editar_materia"),
    path("<uuid:materia_id>/topicos/novo/", views.criar_topico, name="criar_topico"),
    path("<uuid:materia_id>/topicos/<uuid:topico_id>/editar/", views.editar_topico, name="editar_topico"),
    path("<uuid:materia_id>/topicos/<uuid:topico_id>/excluir/", views.excluir_topico, name="excluir_topico"),
    path("<uuid:materia_id>/topicos/<uuid:topico_id>/conteudos/novo/", views.criar_conteudo, name="criar_conteudo"),
    path("<uuid:materia_id>/conteudos/<uuid:conteudo_id>/editar/", views.editar_conteudo, name="editar_conteudo"),
    path("<uuid:materia_id>/conteudos/<uuid:conteudo_id>/excluir/", views.excluir_conteudo, name="excluir_conteudo"),
    path("conteudos/<uuid:conteudo_id>/arquivo/", views.baixar_conteudo, name="baixar_conteudo"),
]
