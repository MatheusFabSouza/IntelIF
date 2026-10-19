import uuid

from django.core.validators import FileExtensionValidator
from django.db import models


class Usuario(models.Model):

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

    email = models.EmailField()

    matricula = models.CharField(
        max_length=30,
        blank=True
    )

    tipo_usuario = models.CharField(
        max_length=50
    )

    categoria = models.CharField(
        max_length=100,
        blank=True
    )

    campus = models.CharField(
        max_length=100,
        blank=True
    )

    curso = models.CharField(
        max_length=150,
        blank=True
    )

    turma = models.CharField(
        max_length=100,
        blank=True
    )

    foto = models.URLField(
        blank=True
    )

    foto_perfil = models.FileField(
        upload_to="usuarios/fotos/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )

    def __str__(self):
        return self.nome
