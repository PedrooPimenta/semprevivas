
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
    re_path(r"^register/", views.register, name="register"),
]
