from django import forms
from django.core.validators import RegexValidator

from .models import ConteudoMateria, Materia, Topico


class MateriaPersonalizacaoForm(forms.ModelForm):
    cor = forms.CharField(
        validators=[RegexValidator(r"^#[0-9A-Fa-f]{6}$", "Informe uma cor válida.")]
    )
    limpar_icone_imagem = forms.BooleanField(required=False)

    class Meta:
        model = Materia
        fields = ["cor", "descricao_pessoal", "icone", "icone_imagem"]
        widgets = {
            "descricao_pessoal": forms.Textarea(attrs={"rows": 4, "maxlength": 500}),
            "icone_imagem": forms.FileInput(attrs={"accept": ".png,.jpg,.jpeg,.svg"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._icone_imagem_original = self.instance.icone_imagem.name if self.instance.pk and self.instance.icone_imagem else ""

    def clean_icone_imagem(self):
        imagem = self.cleaned_data.get("icone_imagem")
        if imagem and imagem.size > 2 * 1024 * 1024:
            raise forms.ValidationError("A imagem deve ter no máximo 2 MB.")
        return imagem

    def save(self, commit=True):
        materia = super().save(commit=False)
        arquivo_antigo = self._icone_imagem_original
        novo_arquivo = self.cleaned_data.get("icone_imagem")
        limpar_imagem = self.cleaned_data.get("limpar_icone_imagem")
        arquivo_novo_enviado = bool(novo_arquivo and not getattr(novo_arquivo, "_committed", False))

        excluir_arquivo_antigo = bool(arquivo_antigo and (limpar_imagem or arquivo_novo_enviado))
        if limpar_imagem and not arquivo_novo_enviado:
            materia.icone_imagem = ""

        if commit:
            materia.save()
            if excluir_arquivo_antigo:
                Materia._meta.get_field("icone_imagem").storage.delete(arquivo_antigo)
        return materia


class TopicoForm(forms.ModelForm):

    class Meta:
        model = Topico
        fields = ["titulo"]
        labels = {
            "titulo": "Nome do tópico",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ex.: Fundamentos da Idade Moderna"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_css_classes()

    def apply_css_classes(self):
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ConteudoMateriaForm(forms.ModelForm):

    class Meta:
        model = ConteudoMateria
        fields = ["titulo", "tipo", "arquivo", "link", "anotacao", "periodo"]
        labels = {
            "titulo": "Título",
            "tipo": "Tipo de conteúdo",
            "arquivo": "Arquivo",
            "link": "Endereço do link",
            "anotacao": "Anotação",
            "periodo": "Bimestre/Período (opcional)",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ex.: Slides da aula 1"}),
            "tipo": forms.Select(attrs={"data-content-type": "true"}),
            "arquivo": forms.ClearableFileInput(attrs={"accept": ".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.odt,.ods,.odp,.txt,.md,.png,.jpg,.jpeg"}),
            "link": forms.URLInput(attrs={"placeholder": "https://"}),
            "anotacao": forms.Textarea(attrs={"rows": 5, "placeholder": "Escreva sua anotação"}),
            "periodo": forms.TextInput(attrs={"placeholder": "Ex.: 1º Bimestre"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._arquivo_original = self.instance.arquivo.name if self.instance.pk and self.instance.arquivo else ""
        self.fields["arquivo"].required = False
        self.fields["link"].required = False
        self.fields["anotacao"].required = False
        self.fields["arquivo"].help_text = "Formatos aceitos: PDF, documentos, planilhas, apresentações e imagens."
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get("tipo")

        if tipo == ConteudoMateria.TIPO_ARQUIVO:
            arquivo = cleaned.get("arquivo")
            clear_checked = self.data.get(self.add_prefix("arquivo") + "-clear")
            if not arquivo and not clear_checked and self.instance.pk:
                arquivo = getattr(self.instance, "arquivo", None)
            if not arquivo:
                self.add_error("arquivo", "Selecione um arquivo.")
        elif tipo == ConteudoMateria.TIPO_LINK and not cleaned.get("link"):
            self.add_error("link", "Informe o endereço do link.")
        elif tipo == ConteudoMateria.TIPO_ANOTACAO and not cleaned.get("anotacao", "").strip():
            self.add_error("anotacao", "Escreva o conteúdo da anotação.")

        return cleaned

    def save(self, commit=True):
        conteudo = super().save(commit=False)

        if conteudo.tipo != ConteudoMateria.TIPO_ARQUIVO:
            conteudo.arquivo = ""
        if conteudo.tipo != ConteudoMateria.TIPO_LINK:
            conteudo.link = ""
        if conteudo.tipo != ConteudoMateria.TIPO_ANOTACAO:
            conteudo.anotacao = ""

        if commit:
            conteudo.save()
            self.save_m2m()
            arquivo_atual = conteudo.arquivo.name if conteudo.arquivo else ""
            if self._arquivo_original and self._arquivo_original != arquivo_atual:
                ConteudoMateria._meta.get_field("arquivo").storage.delete(self._arquivo_original)
        return conteudo
