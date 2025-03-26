from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetCompleteView

from django.urls import reverse_lazy,reverse
from django.contrib.auth import logout
from django.contrib.auth import login

from django.core.exceptions import PermissionDenied

from .forms import CustomUserCreationForm

def register(request):
    if request.method == "GET":
        # Se for um GET, renderize o formulário vazio
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm()}
        )

    elif request.method == "POST":
        # Quando for um POST, processe o formulário
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()  # Salva o novo usuário
            login(request, user)  # Faz login automaticamente
            return redirect(reverse("dashboard"))  # Redireciona para o dashboard

        else:
            # Se o formulário for inválido, renderize novamente o formulário com erros
            return render(
                request, "registration/register.html", 
                {"form": form}  # Passa o formulário com os erros
            )


class CustomPasswordChangeView(PasswordChangeView):
    print("Entrou na função para alterar a senha")
    template_name = 'registration/alterar_senha.html'
    success_url = reverse_lazy('senha_alterada')  # Defina a página para redirecionar após a alteração da senha
    
# Create your views here.
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/senha_alterada.html'
    success_url = reverse_lazy('dashboard')  # Defina a página para redirecionar após a alteração da senha



class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('custom_reset_password_done')  # Defina a página para redirecionar após a alteração da senha
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    success_url = reverse_lazy('dashboard')  # Defina a página para redirecionar após a alteração da senha   
    


@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

def minha_view_protegida(request):
    try:
        # Conteúdo da sua view protegida
        ...
    except PermissionDenied:
        # Processar o erro de permissão negada aqui
        return render(request, 'erro_autenticacao.html')


