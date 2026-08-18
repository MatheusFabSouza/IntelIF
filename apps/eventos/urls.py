from django.urls import path
from . import views


app_name = "eventos"

urlpatterns = [
    path("criar/", views.criar_evento, name="criar_evento"),
    path("", views.lista_eventos, name="listar_eventos"),
    path("editar/<uuid:id>/", views.editar_evento, name="editar_evento"),
    path("excluir/<uuid:id>/", views.excluir_evento, name="excluir_evento"),
]