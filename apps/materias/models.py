import uuid
import random
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator


CORES_MATERIA = ["#A78BFA", "#2563EB", "#F97316", "#EF4444", "#EC4899"]


def cor_aleatoria_materia():
    return random.choice(CORES_MATERIA)


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

    ICONE_CHOICES = [
        ("", "Sem ícone"),
        ("calculator", "Calculadora"),
        ("globe", "Globo"),
        ("database", "Banco de dados"),
        ("book", "Livro"),
        ("flask", "Ciências"),
        ("code", "Programação"),
        ("atom", "Átomo"),
        ("leaf", "Natureza"),
    ]

    STATUS_CHOICES = [
        ("bom", "Bom"),
        ("regular", "Regular"),
        ("ruim", "Ruim"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id_suap = models.IntegerField()

    descricao = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="regular"
    )

    cor = models.CharField(
        max_length=7,
        default=cor_aleatoria_materia,
        validators=[RegexValidator(r"^#[0-9A-Fa-f]{6}$", "Informe uma cor hexadecimal válida.")],
    )

    descricao_pessoal = models.TextField(blank=True)

    icone = models.CharField(max_length=20, choices=ICONE_CHOICES, blank=True, default="")

    icone_imagem = models.FileField(
        upload_to="materias/icones/",
        blank=True,
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "svg"])],
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

    @property
    def icone_css_class(self):
        classes = {
            "calculator": "fa-solid fa-calculator",
            "globe": "fa-solid fa-globe",
            "database": "fa-solid fa-database",
            "book": "fa-solid fa-book",
            "flask": "fa-solid fa-flask",
            "code": "fa-solid fa-code",
            "atom": "fa-solid fa-atom",
            "leaf": "fa-solid fa-leaf",
        }
        return classes.get(self.icone, "")


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


class Topico(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name="topicos"
    )

    titulo = models.CharField(max_length=160)

    descricao = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo


class ConteudoMateria(models.Model):

    TIPO_ARQUIVO = "arquivo"
    TIPO_LINK = "link"
    TIPO_ANOTACAO = "anotacao"
    TIPOS = [
        (TIPO_ARQUIVO, "Arquivo"),
        (TIPO_LINK, "Link"),
        (TIPO_ANOTACAO, "Anotação"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    topico = models.ForeignKey(
        Topico,
        on_delete=models.CASCADE,
        related_name="conteudos"
    )

    titulo = models.CharField(max_length=200)

    tipo = models.CharField(max_length=12, choices=TIPOS)

    arquivo = models.FileField(
        upload_to="materias/conteudos/",
        blank=True,
        validators=[FileExtensionValidator([
            "pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx",
            "odt", "ods", "odp", "txt", "md", "png", "jpg", "jpeg"
        ])]
    )

    link = models.URLField(max_length=1000, blank=True)

    anotacao = models.TextField(blank=True)

    periodo = models.CharField(max_length=40, blank=True)

    adicionado_em = models.DateTimeField(auto_now_add=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-adicionado_em"]

    def __str__(self):
        return self.titulo

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
