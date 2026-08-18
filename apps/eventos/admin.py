from django.contrib import admin

from django.contrib import admin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "data",
        "horario",
        "visibilidade",
        "criador",
        "turma",
    )

    list_filter = (
        "categoria",
        "visibilidade",
    )

    search_fields = (
        "titulo",
        "descricao",
    )
