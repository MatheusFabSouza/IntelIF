from django import forms
from .models import Evento


class EventoForm(forms.ModelForm):

    class Meta:
        model = Evento
        fields = [
            "titulo",
            "descricao",
            "categoria",
            "data",
            "horario",
            "visibilidade",
            "turma",
        ]
        labels = {
            "titulo": "Título",
            "descricao": "Descrição",
            "categoria": "Categoria",
            "data": "Data",
            "horario": "Horário",
            "visibilidade": "Visibilidade",
            "turma": "Turma",
        }
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "data": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "horario": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget
            css_class = "form-select" if isinstance(widget, forms.Select) else "form-control"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css_class}".strip()

        self.fields["titulo"].widget.attrs.setdefault("placeholder", "Ex.: Prova de Matemática")
        self.fields["descricao"].widget.attrs.setdefault("placeholder", "Adicione detalhes importantes (opcional)")
        self.fields["turma"].widget.attrs.setdefault("placeholder", "Ex.: INFO3V")
