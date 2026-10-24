from django import forms
from .models import Colaborador, EPI


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ["nome", "cpf", "setor", "status"]

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError("Informe os 11 dígitos do CPF, só números.")
        return cpf


class EPIForm(forms.ModelForm):
    class Meta:
        model = EPI
        fields = ["nome", "categoria", "estoque"]