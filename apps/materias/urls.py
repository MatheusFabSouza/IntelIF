from django.urls import path
from . import views


app_name = "materias"

urlpatterns = [
    path("", views.lista_materias, name="listar_materias"),
]