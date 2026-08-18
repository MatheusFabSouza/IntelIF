import uuid
from django.db import models


class Evento(models.Model):

    VISIBILIDADE_CHOICES = [
        ("PESSOAL", "Apenas para mim"),
        ("TURMA", "Para turma"),
        ("TODOS", "Todos os alunos"),
    ]

    CATEGORIA_CHOICES = [
        ("PROVA", "Prova"),
        ("TRABALHO", "Trabalho"),
        ("ATIVIDADE", "Atividade"),
        ("ESTUDO", "Estudo"),
        ("PESSOAL", "Pessoal"),
        ("OUTRO", "Outro"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    titulo = models.CharField(
        max_length=150
    )

    descricao = models.TextField(
        blank=True
    )

    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIA_CHOICES
    )

    data = models.DateField()

    horario = models.TimeField()

    criador = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.CASCADE,
        related_name="eventos"
    )

    visibilidade = models.CharField(
        max_length=20,
        choices=VISIBILIDADE_CHOICES
    )

    turma = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.titulo