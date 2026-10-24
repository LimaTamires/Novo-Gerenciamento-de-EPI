from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ColaboradorForm, EPIForm, EmprestimoForm, ItemFormSet, DevolucaoForm
from .models import Colaborador, EPI, ItemEmprestimo, Emprestimo
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import F

def home(req):
    return render(req, 'nucleo/base.html')

# ---------- Colaboradores ----------
class ColaboradorList(CreateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = "nucleo/colaborador_lista.html"
    success_url = reverse_lazy("nucleo:colaborador_lista")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colaboradores"] = Colaborador.objects.select_related("setor")
        return context


class ColaboradorCreate(CreateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = "nucleo/form.html"
    success_url = reverse_lazy("nucleo:colaborador_lista")
    extra_context = {"titulo": "Novo colaborador"}


class ColaboradorUpdate(UpdateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = "nucleo/form.html"
    success_url = reverse_lazy("nucleo:colaborador_lista")
    extra_context = {"titulo": "Editar colaborador"}


class ColaboradorDelete(DeleteView):
    model = Colaborador
    template_name = "nucleo/confirmar_exclusao.html"
    success_url = reverse_lazy("nucleo:colaborador_lista")


# ---------- EPIs ----------
class EPIList(CreateView):
    model = EPI
    form_class = EPIForm
    template_name = "nucleo/epi_lista.html"
    success_url = reverse_lazy("nucleo:epi_lista")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["epis"] = EPI.objects.select_related("categoria")
        return context


class EPICreate(CreateView):
    model = EPI
    form_class = EPIForm
    template_name = "nucleo/form.html"
    success_url = reverse_lazy("nucleo:epi_lista")
    extra_context = {"titulo": "Novo EPI"}


class EPIUpdate(UpdateView):
    model = EPI
    form_class = EPIForm
    template_name = "nucleo/form.html"
    success_url = reverse_lazy("nucleo:epi_lista")
    extra_context = {"titulo": "Editar EPI"}


class EPIDelete(DeleteView):
    model = EPI
    template_name = "nucleo/confirmar_exclusao.html"
    success_url = reverse_lazy("nucleo:epi_lista")

# ---------- Empréstimos ----------
class EmprestimoList(ListView):
    model = ItemEmprestimo
    template_name = "nucleo/emprestimo_lista.html"
    context_object_name = "itens"

    def get_queryset(self):
        return (
            ItemEmprestimo.objects
            .select_related("emprestimo__colaborador", "epi")
            .order_by("-emprestimo__data_emprestimo", "-id")
        )


class EmprestimoCreate(CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "nucleo/emprestimo_form.html"
    success_url = reverse_lazy("nucleo:emprestimo_lista")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["formset"] = ItemFormSet(self.request.POST)
        else:
            context["formset"] = ItemFormSet()
        return context

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        if not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            for item in formset.save():
                EPI.objects.filter(pk=item.epi_id).update(
                    estoque=F("estoque") - item.quantidade
                )
        return redirect(self.success_url)


class ItemDevolver(UpdateView):
    model = ItemEmprestimo
    form_class = DevolucaoForm
    template_name = "nucleo/form.html"
    success_url = reverse_lazy("nucleo:emprestimo_lista")
    extra_context = {"titulo": "Registrar devolução"}

    def get_queryset(self):
        # só itens ainda não devolvidos (evita devolver duas vezes)
        return ItemEmprestimo.objects.filter(data_devolucao__isnull=True)

    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            if self.object.condicao_devolucao == ItemEmprestimo.Condicao.BOA:
                EPI.objects.filter(pk=self.object.epi_id).update(
                    estoque=F("estoque") + self.object.quantidade
                )
        return response