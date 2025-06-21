from django.shortcuts import render, redirect, get_object_or_404
from .models import Pesquisador
from .forms import PesquisadorForm
from django.contrib.auth.decorators import login_required

@login_required
def listar_equipe(request):
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)

    pesquisadores = Pesquisador.objects.filter(ativo=True)
    return render(request, 'equipe.html', {'pesquisadores': pesquisadores})

@login_required
def adicionar_pesquisador(request):
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)

    if request.method == "POST":
        form = PesquisadorForm(request.POST)
        if form.is_valid():
            pesquisador = form.save(commit=False)
            pesquisador.ativo = True
            pesquisador.save()
            return redirect("listar_equipe")
    else:
        form = PesquisadorForm()

    return render(request, "adicionar_pesquisador.html", {"form": form})

@login_required(login_url='/usuarios/contas/login')
def editar_pesquisador(request, pesquisador_id):
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)

    pesquisador = get_object_or_404(Pesquisador, pk=pesquisador_id)

    if request.method == 'POST':
        form = PesquisadorForm(request.POST, instance=pesquisador)
        if form.is_valid():
            form.save()
            return redirect('listar_equipe')
    else:
        form = PesquisadorForm(instance=pesquisador)

    return render(request, 'editar_pesquisador.html', {'form': form})

@login_required
def apagar_pesquisador(request, pesquisador_id):
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)

    pesquisador = get_object_or_404(Pesquisador, pk=pesquisador_id)

    if request.method == 'POST':
        pesquisador.delete()
        return redirect('listar_equipe')

    return render(request, 'confirma_exclusao.html', {'pesquisador': pesquisador})
