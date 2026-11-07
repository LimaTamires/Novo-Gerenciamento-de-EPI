from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_not_required



app_name = "nucleo"

urlpatterns = [
        # ----- Autenticação -----
    path(
        "login/",
        login_not_required(
            auth_views.LoginView.as_view(
                template_name="nucleo/login.html",
                redirect_authenticated_user=True,
            )
        ),
        name="login",
    ),
    path("logout/", login_not_required(auth_views.LogoutView.as_view()), name="logout"),
    path("colaboradores/", views.ColaboradorList.as_view(), name="colaborador_lista"),
    path("colaboradores/novo/", views.ColaboradorCreate.as_view(), name="colaborador_novo"),
    path("colaboradores/<int:pk>/editar/", views.ColaboradorUpdate.as_view(), name="colaborador_editar"),
    path("colaboradores/<int:pk>/excluir/", views.ColaboradorDelete.as_view(), name="colaborador_excluir"),
    path("epis/", views.EPIList.as_view(), name="epi_lista"),
    path("epis/novo/", views.EPICreate.as_view(), name="epi_novo"),
    path("epis/<int:pk>/editar/", views.EPIUpdate.as_view(), name="epi_editar"),
    path("epis/<int:pk>/excluir/", views.EPIDelete.as_view(), name="epi_excluir"),
    path("", views.home, name="home"),
    path("emprestimos/", views.EmprestimoList.as_view(), name="emprestimo_lista"),
    path("emprestimos/novo/", views.EmprestimoCreate.as_view(), name="emprestimo_novo"),
    path("emprestimos/item/<int:pk>/devolver/", views.ItemDevolver.as_view(), name="item_devolver"),
]