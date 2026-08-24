import uuid
from django.db import models


class Professor(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id_suap = models.IntegerField(
        unique=True
    )

    nome = models.CharField(
        max_length=150
    )

    def __str__(self):
        return self.nome


class Materia(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id_suap = models.IntegerField()

    descricao = models.CharField(
        max_length=200
    )

    usuario = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.CASCADE,
        related_name="materias"
    )

    professores = models.ManyToManyField(
        Professor,
        related_name="materias",
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id_suap", "usuario"],
                name="materia_unica_por_usuario"
            )
        ]

    def __str__(self):
        return self.descricao


class HorarioMateria(models.Model):

    DIAS_SEMANA = [
        ("Segunda", "Segunda"),
        ("Terça", "Terça"),
        ("Quarta", "Quarta"),
        ("Quinta", "Quinta"),
        ("Sexta", "Sexta"),
        ("Sábado", "Sábado"),
        ("Domingo", "Domingo"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name="horarios"
    )

    dia = models.CharField(
        max_length=10,
        choices=DIAS_SEMANA
    )

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.materia} - {self.dia} {self.hora_inicio} - {self.hora_fim}"

class AtividadeClassroom(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id_classroom = models.CharField(
        max_length=100,
        unique=True
    )

    titulo = models.CharField(
        max_length=300
    )

    data_entrega = models.DateTimeField(
        null=True,
        blank=True
    )

    link = models.URLField(
        max_length=500,
        blank=True
    )

    curso_classroom_id = models.CharField(
        max_length=100
    )

    curso_nome = models.CharField(
        max_length=300,
        blank=True
    )

    usuario = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.CASCADE,
        related_name="atividades_classroom"
    )

    def __str__(self):
        return self.titulo
