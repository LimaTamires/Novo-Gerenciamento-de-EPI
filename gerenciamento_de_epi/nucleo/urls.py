from django.urls import path
from . import views
from django.views.generic import RedirectView


app_name = "nucleo"

urlpatterns = [
    path("colaboradores/", views.ColaboradorList.as_view(), name="colaborador_lista"),
    path("colaboradores/novo/", views.ColaboradorCreate.as_view(), name="colaborador_novo"),
    path("colaboradores/<int:pk>/editar/", views.ColaboradorUpdate.as_view(), name="colaborador_editar"),
    path("colaboradores/<int:pk>/excluir/", views.ColaboradorDelete.as_view(), name="colaborador_excluir"),

    path("epis/", views.EPIList.as_view(), name="epi_lista"),
    path("epis/novo/", views.EPICreate.as_view(), name="epi_novo"),
    path("epis/<int:pk>/editar/", views.EPIUpdate.as_view(), name="epi_editar"),
    path("epis/<int:pk>/excluir/", views.EPIDelete.as_view(), name="epi_excluir"),
    path("", views.home, name="home"),
]