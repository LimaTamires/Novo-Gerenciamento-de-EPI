from django.contrib import admin
from .models import Setor, Colaborador, EPICategoria, EPI

admin.site.register([Setor, Colaborador, EPICategoria, EPI])