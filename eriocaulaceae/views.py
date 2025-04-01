from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse

from .forms import TaxonForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CSVUploadForm
import csv
import io  
from io import TextIOWrapper
import pandas as pd
from .models import Taxon
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .forms import TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form,TaxonStep6Form,TaxonStep7Form,TaxonStep8Form,TaxonStep9Form
from formtools.wizard.views import SessionWizardView
from django.db.models import Q

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
            return redirect('eriocaulaceae_home')  #
    else:
        form = TaxonForm()
    return render(request, 'eriocaulaceae_adicionar.html', {'form': form})

@login_required
def listar_especies(request):
    # Pega o termo de busca da query string (GET)
    termo_busca = request.GET.get('q', '')

    # Filtra os resultados com base no termo de busca
    queryset = Taxon.objects.all()

    if termo_busca:
        queryset = queryset.filter(
            Q(scientificName__icontains=termo_busca) |
            Q(acceptedNameUsage__icontains=termo_busca)
        )

    # Paginação
    paginator = Paginator(queryset, 5)  # Exibe 5 itens por página
    page_number = request.GET.get('page')  # Número da página
    page_obj = paginator.get_page(page_number)

    # Dicionário de estados
    estados = {
        'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia',
        'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
        'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
        'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
        'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
    }

    # Processar estado para nomes completos
    for taxon in page_obj:
        if taxon.estado is not None:
            nomes_completos = [estados.get(sigla) for sigla in eval(taxon.estado)]
            taxon.estado = nomes_completos
        else:
            taxon.estado = None

    # Passar os dados para o template
    return render(request, 'listar_especies.html', {'page_obj': page_obj, 'termo_busca': termo_busca})
        
    



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
            return redirect('buscar_especies')  
    else:
        form = TaxonForm(instance=especie)
    return render(request, 'editar_especie.html', {'form': form})

    

def apagar_especie(request, especie_id):
    especie = get_object_or_404(Taxon, id=especie_id)
    if request.method == 'POST':
        especie.delete()
        return redirect('listar_especies')  
    else:
        return render(request, 'apagar_especie.html', {'especie': especie})



def adicionar_especie(request):
    if request.method == 'POST':
        form = TaxonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_especies')  
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


class EditTaxonWizard(SessionWizardView):
    form_list = [TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form, TaxonStep9Form]
    template_name = "edit_taxon_wizard.html"
    file_storage = FileSystemStorage(location='/tmp')
    def get_wizard_kwargs(self, step):
        """
        Garante que o 'pk' seja passado corretamente para o método 'done'.
        """
        kwargs = super().get_wizard_kwargs(step)
        kwargs['pk'] = self.kwargs.get('pk')  # Captura o 'pk' da URL
        return kwargs
    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step)
        taxon_id = self.kwargs.get('pk')
        if taxon_id:
            taxon = Taxon.objects.get(pk=taxon_id)
            kwargs['instance'] = taxon
        return kwargs


    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        taxon_id = self.kwargs.get('pk')
        if not taxon_id:
            raise ValueError("ID do táxon não encontrado na URL")
        taxon = Taxon.objects.get(pk=taxon_id)
        taxon.taxonID = data['taxonID']
        taxon.acceptedNameUsageID = data['acceptedNameUsageID']
        taxon.parentNameUsageID = data['parentNameUsageID']
        taxon.originalNameUsageID = data['originalNameUsageID']
        taxon.scientificName = data['scientificName']
        taxon.acceptedNameUsage = data['acceptedNameUsage']
        taxon.parentNameUsage = data['parentNameUsage']
        taxon.namePublishedIn = data['namePublishedIn']
        taxon.namePublishedInYear = data['namePublishedInYear']
        taxon.higherClassification = data['higherClassification']
        taxon.kingdom = data['kingdom']
        taxon.phylum = data['phylum']
        taxon.classe = data['classe']
        taxon.order = data['order']
        taxon.family = data['family']
        taxon.genus = data['genus']
        taxon.specificEpithet = data['specificEpithet']
        taxon.infraspecificEpithet = data['infraspecificEpithet']
        taxon.taxonRank = data['taxonRank']
        taxon.bibliographicCitation = data['bibliographicCitation']
        taxon.references = data['references']
        taxon.foto = data['foto']

        taxon.save()

        messages.success(self.request, 'Atualização realizada com sucesso.')

        form_list = [form.__class__() for form in form_list]

        return render(self.request, self.template_name, {
            'wizard': self,
            'form_list': form_list,
            'taxon': taxon,
        })