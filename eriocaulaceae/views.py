from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse

from .forms import TaxonForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CSVUploadForm
import csv
import io  # Importe o módulo io para lidar com arquivos de texto
from io import TextIOWrapper
import pandas as pd
from .models import Taxon
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .forms import TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form,TaxonStep6Form,TaxonStep7Form,TaxonStep8Form,TaxonStep9Form
from formtools.wizard.views import SessionWizardView

import json 


# Create your views here.
def eriocaulaceae_home(request):
    return render(request,"eriocaulaceae_home.html")

@login_required
def eriocaulaceae_adicionar(request):
    if request.method == 'POST':
        form = TaxonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eriocaulaceae_home')  # Redirecionar para a página de lista de taxons após adicionar com sucesso
    else:
        form = TaxonForm()
    return render(request, 'eriocaulaceae_adicionar.html', {'form': form})

@login_required
def listar_especies(request):
    especies = Taxon.objects.all()
    
    paginator = Paginator(especies, 5)  # 10 por página
    page_number = request.GET.get('page')  # Obtendo o número da página da URL
    page_obj = paginator.get_page(page_number)  # Obtendo a página atual

    estados = {
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins',
    }

    for taxon in page_obj:
        if taxon.estado is not None:
            nomes_completos = [estados.get(sigla) for sigla in eval(taxon.estado)]
            taxon.estado = nomes_completos
        else:
            taxon.estado = None

    return render(request, 'listar_especies.html', {'page_obj': page_obj})



@login_required
def buscar_especies(request):
    especies = []
    termo_busca = 'Erio'

    if request.method == 'POST':
        termo_busca = request.POST.get('termo_busca')
        especies = Taxon.objects.filter(Q(scientificName__icontains=termo_busca) | Q(acceptedNameUsage__icontains=termo_busca)
        )

    return render(request, 'buscar_especies.html', {'especies': especies, 'termo_busca': termo_busca})


def editar_especie(request, especie_id):
    especie = get_object_or_404(Taxon, id=especie_id)
    if request.method == 'POST':
        form = TaxonForm(request.POST, instance=especie)
        if form.is_valid():
            form.save()
            return redirect('buscar_especies')  # Redireciona de volta para a página de busca após a edição
    else:
        form = TaxonForm(instance=especie)
    return render(request, 'editar_especie.html', {'form': form})

    

def apagar_especie(request, especie_id):
    especie = get_object_or_404(Taxon, id=especie_id)
    if request.method == 'POST':
        especie.delete()
        return redirect('listar_especies')  # Redireciona de volta para a página de busca após a exclusão
    else:
        return render(request, 'apagar_especie.html', {'especie': especie})



def adicionar_especie(request):
    if request.method == 'POST':
        form = TaxonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_especies')  # Redireciona para a página de sucesso após adicionar o Taxon
    else:
        form = TaxonForm()
    return render(request, 'adicionar_especie.html', {'form': form})




def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo_csv']
            if arquivo.name.endswith('.csv'):
                df=pd.read_csv(arquivo,sep=';')
                df.fillna(value='-1', inplace=True)
                for index, linha in df.iterrows():
                    taxon = Taxon(
                        taxonID=linha['taxonID'],
                        acceptedNameUsageID=linha['acceptedNameUsageID'],
                        parentNameUsageID=linha['parentNameUsageID'],
                        originalNameUsageID=linha['originalNameUsageID'],
                        scientificName=linha['scientificName'],
                        acceptedNameUsage=linha['acceptedNameUsage'],
                        parentNameUsage=linha['parentNameUsage'],
                        namePublishedIn=linha['namePublishedIn'],
                        namePublishedInYear=linha['namePublishedInYear'],
                        higherClassification=linha['higherClassification'],
                        kingdom=linha['kingdom'],
                        phylum=linha['phylum'],
                        classe=linha['classe'],
                        order=linha['order'],
                        family=linha['family'],
                        genus=linha['genus'],
                        specificEpithet=linha['specificEpithet'],
                        infraspecificEpithet=linha['infraspecificEpithet'],
                        taxonRank=linha['taxonRank'],
                        scientificNameAuthorship=linha['scientificNameAuthorship'],
                        taxonomicStatus=linha['taxonomicStatus'],
                        nomenclaturalStatus=linha['nomenclaturalStatus'],
                        modified=linha['modified'],
                        bibliographicCitation=linha['bibliographicCitation'],
                        references=linha['references']
                    )
                    taxon.save()
                
                
                return render(request, 'sucesso.html')
            else:
                return render(request, 'erro.html', {'mensagem': 'O arquivo enviado não é um arquivo CSV.'})
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})



class TaxonWizard(SessionWizardView):
    form_list = [TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form, TaxonStep9Form]
    template_name = "taxon_form_wizard.html"
    file_storage = FileSystemStorage(location='/tmp')

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        taxon = Taxon.objects.create(**data)

        messages.success(self.request, 'Cadastro realizado com sucesso.')

        form_list = [form.__class__() for form in form_list]

        return render(self.request, self.template_name, {
            'wizard': self,
            'form_list': form_list
        })