from django import forms
from .models import Colaborador, EPI, Emprestimo, ItemEmprestimo
from django.forms import inlineformset_factory
from django.utils import timezone


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





class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ["colaborador", "data_emprestimo", "observacao"]
        widgets = {
            "data_emprestimo": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # só colaboradores ativos podem pegar EPI
        self.fields["colaborador"].queryset = Colaborador.objects.filter(status=True)


class ItemEmprestimoForm(forms.ModelForm):
    class Meta:
        model = ItemEmprestimo
        fields = ["epi", "quantidade"]

    def clean(self):
        cleaned = super().clean()
        epi = cleaned.get("epi")
        qtd = cleaned.get("quantidade")
        if epi and qtd and qtd > epi.estoque:
            raise forms.ValidationError(
                f"Estoque insuficiente de {epi.nome}: disponível {epi.estoque}."
            )
        return cleaned


ItemFormSet = inlineformset_factory(
    Emprestimo,
    ItemEmprestimo,
    form=ItemEmprestimoForm,
    extra=2,
    min_num=1,
    validate_min=True,
    can_delete=False,
)


class DevolucaoForm(forms.ModelForm):
    class Meta:
        model = ItemEmprestimo
        fields = ["data_devolucao", "condicao_devolucao"]
        widgets = {
            "data_devolucao": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_devolucao"].required = True
        self.fields["data_devolucao"].initial = timezone.localdate
        self.fields["condicao_devolucao"].required = True

    def clean_data_devolucao(self):
        data = self.cleaned_data["data_devolucao"]
        if data < self.instance.emprestimo.data_emprestimo:
            raise forms.ValidationError("A devolução não pode ser antes do empréstimo.")
        return data