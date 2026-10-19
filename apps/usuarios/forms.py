from django import forms
from django.core.validators import FileExtensionValidator


class FotoPerfilForm(forms.Form):
    foto = forms.FileField(
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        error_messages={"required": "Escolha uma foto para enviar."},
    )

    def clean_foto(self):
        foto = self.cleaned_data["foto"]
        if foto.size > 2 * 1024 * 1024:
            raise forms.ValidationError("A foto deve ter no máximo 2 MB.")
        assinatura = foto.read(8)
        foto.seek(0)
        extensao = foto.name.rsplit(".", 1)[-1].lower()
        if extensao in {"jpg", "jpeg"} and not assinatura.startswith(b"\xff\xd8\xff"):
            raise forms.ValidationError("O arquivo selecionado não parece ser uma imagem JPG válida.")
        if extensao == "png" and assinatura != b"\x89PNG\r\n\x1a\n":
            raise forms.ValidationError("O arquivo selecionado não parece ser uma imagem PNG válida.")
        return foto
