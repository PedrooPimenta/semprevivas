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

from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm()}
        )

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()  

            try:
                grupo_convidado = Group.objects.get(name='Convidado')
                user.groups.add(grupo_convidado)
            except Group.DoesNotExist:
                pass  

            login(request, user)  
            return redirect(reverse("dashboard"))

        return render(
            request, "registration/register.html",
            {"form": form}
        )


class CustomPasswordChangeView(PasswordChangeView):
    print("Entrou na função para alterar a senha")
    template_name = 'registration/alterar_senha.html'
    success_url = reverse_lazy('senha_alterada') 
    
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/senha_alterada.html'
    success_url = reverse_lazy('dashboard') 



class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('custom_reset_password_done')  
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    success_url = reverse_lazy('dashboard') 
    


@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

def minha_view_protegida(request):
    try:
       
        ...
    except PermissionDenied:
        return render(request, 'erro_autenticacao.html')



@login_required
def listar_usuarios(request):
    if not request.user.groups.filter(name='Adm').exists():
        return render(request, 'access_denied.html', status=403)

    User = get_user_model()
    usuarios = User.objects.all().order_by('username')
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios_page = paginator.get_page(page_number)

    return render(request, 'listar_usuarios.html', {'usuarios': usuarios_page})

login_required
def editar_usuario(request, user_id):
    if not request.user.groups.filter(name='Adm').exists():
        return render(request, 'access_denied.html', status=403)

    User = get_user_model()
    usuario = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def apagar_usuario(request, user_id):
    if not request.user.groups.filter(name='Adm').exists():
        return render(request, 'access_denied.html', status=403)

    User = get_user_model()
    usuario = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')

    return render(request, 'confirmar_exclusao.html', {'usuario': usuario})

@login_required
def atribuir_grupo(request, user_id, group_name):
    if not request.user.groups.filter(name='Adm').exists():
        raise PermissionDenied("Você não tem permissão para acessar esta página.")

    User = get_user_model()
    usuario = get_object_or_404(User, pk=user_id)
    grupo = get_object_or_404(Group, name=group_name)

    if request.method == 'POST':
        
        usuario.groups.clear()
        usuario.groups.add(grupo)
        return redirect('listar_usuarios')

    return render(request, 'atribuir_grupo.html', {'usuario': usuario, 'grupo': grupo})