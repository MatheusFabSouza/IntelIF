from django.urls import path
from . import views


app_name = "materias"

urlpatterns = [
    path("", views.lista_materias, name="listar_materias"),
    path("<uuid:id>/", views.detalhes_materia, name="detalhes_materia"),
]