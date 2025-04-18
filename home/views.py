from django.shortcuts import render

from eriocaulaceae.models import Taxon

def index(request):
    solicitacoes_pendentes = Taxon.objects.filter(status=False).count()

    context = {
        'solicitacoes_pendentes': solicitacoes_pendentes
    }
    
    return render(request, 'index.html', context)


