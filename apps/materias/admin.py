from django.contrib import admin
from .models import Materia, Professor, HorarioMateria, AtividadeClassroom


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("descricao", "usuario")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "id_suap")


@admin.register(HorarioMateria)
class HorarioMateriaAdmin(admin.ModelAdmin):
    list_display = (
        "materia",
        "dia",
        "hora_inicio",
        "hora_fim",
    )

admin.site.register(AtividadeClassroom)