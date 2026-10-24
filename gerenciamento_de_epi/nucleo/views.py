from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ColaboradorForm, EPIForm
from .models import Colaborador, EPI
from django.shortcuts import render, redirect

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