
from django.urls import include, re_path,path
from usuarios.views import CustomPasswordChangeView
from usuarios.views import CustomPasswordChangeDoneView
from usuarios.views import CustomPasswordResetView
from usuarios.views import CustomPasswordResetDoneView
from usuarios.views import CustomPasswordResetCompleteView

from . import views 

urlpatterns = [
    re_path(r"^contas/", include("django.contrib.auth.urls")),
    re_path(r"^dashboard/", views.dashboard, name="dashboard"),
    path('contas/altera_senha/', CustomPasswordChangeView.as_view(), name='altera_senha'),
    path('contas/senha_alterada/', CustomPasswordChangeDoneView.as_view(), name='senha_alterada'),
    path('contas/reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('contas/reset_password_done/', CustomPasswordResetDoneView.as_view(), name='custom_reset_password_done'),
    path('contas/reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='reset_password_complete'),
    path('logout/', views.logout_view, name='logout'),
    path("listar/usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("editar_usuario/<int:user_id>/", views.editar_usuario, name="editar_usuario"),
    path("apagar_usuario/<int:user_id>/", views.apagar_usuario, name="apagar_usuario"),
    path('atribuir_grupo/<int:user_id>/<str:group_name>/', views.atribuir_grupo, name='atribuir_grupo'),

    re_path(r"^register/", views.register, name="register"),

    path('listar_equipe',views.listar_equipe, name='listar_equipe'),

    path('adicionar_pesquisador/',views.adicionar_pesquisador,name='adicionar_pesquisador'),
    path('editar_pesquisador/<int:pesquisador_id>/', views.editar_pesquisador, name='editar_pesquisador'),
    path('apagar_pesquisador/<int:pesquisador_id>/', views.apagar_pesquisador, name='apagar_pesquisador'),
]
