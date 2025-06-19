import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
import pandas as pd
from .forms import (
    TaxonForm, CSVUploadForm,
    TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form,
    TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form, TaxonStep9Form
)
from .models import Taxon

def eriocaulaceae_home(request):
    return render(request, "eriocaulaceae_home.html")

@login_required

def eriocaulaceae_adicionar(request):
    group_required = 'administradores'
    if request.method == 'POST':
        form = TaxonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eriocaulaceae_home')
    else:
        form = TaxonForm()
    return render(request, 'eriocaulaceae_adicionar.html', {'form': form})

def listar_especies(request):
    termo_busca = request.GET.get('q', '')
    queryset = Taxon.objects.filter(status=True)
    solicitacoes_pendentes = Taxon.objects.filter(status=False).count()

    if termo_busca:
        queryset = queryset.filter(
            Q(scientificName__icontains=termo_busca) |
            Q(namePublishedInYear__icontains=termo_busca) |
            Q(genus__icontains=termo_busca) |
            Q(estado__icontains=termo_busca) |
            Q(paises__icontains=termo_busca)
        )

    if not queryset.exists():
        messages.info(request, 'Nenhuma espécie encontrada.')

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    estados = {
        'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia',
        'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
        'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
        'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
        'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
    }

    for taxon in page_obj:
        if taxon.estado:
            nomes_completos = [estados.get(sigla) for sigla in eval(taxon.estado)]
            taxon.estado = nomes_completos
        else:
            taxon.estado = None

    context = {
        'page_obj': page_obj,
        'termo_busca': termo_busca,
        'solicitacoes_pendentes': solicitacoes_pendentes
    }
    return render(request, 'listar_especies.html', context)

@login_required
def buscar_especies(request):
    especies = []
    termo_busca = 'Erio'

    if request.method == 'POST':
        termo_busca = request.POST.get('termo_busca')
        especies = Taxon.objects.filter(
            Q(scientificName__icontains=termo_busca) | Q(acceptedNameUsage__icontains=termo_busca)
        )
    return render(request, 'buscar_especies.html', {'especies': especies, 'termo_busca': termo_busca})

@login_required
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

@login_required
def apagar_especie(request, especie_id):
    especie = get_object_or_404(Taxon, id=especie_id)
    if request.method == 'POST':
        especie.delete()
        return redirect('listar_especies')
    return render(request, 'apagar_especie.html', {'especie': especie})

@login_required
def set_especie_false(request, especie_id):
    especie = get_object_or_404(Taxon, id=especie_id)
    if request.method == 'POST':
        especie.status = False
        especie.save()
        return redirect('listar_especies')
    return render(request, 'apagar_especie.html', {'especie': especie})

@login_required
def toggle_status(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    taxon.status = not taxon.status
    taxon.save()
    return redirect('listar_solicitacoes')

@login_required
def list_solicitacoes(request):
    solicitacoes = Taxon.objects.filter(status=False)
    return render(request, 'list_solicitacoes.html', {'solicitacoes': solicitacoes})

@login_required
def adicionar_especie(request):
    if request.method == 'POST':
        form = TaxonForm(request.POST)
        if form.is_valid():
            taxon_obj = form.save(commit=False)
            taxon_obj.status = False
            taxon_obj.save()
            messages.info(request, 'Seu cadastro será verificado por um administrador.')
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
                df = pd.read_csv(arquivo, sep=';')
                df.fillna(value='-1', inplace=True)
                for _, linha in df.iterrows():
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
    form_list = [
        TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form,
        TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form,
        TaxonStep9Form
    ]
    template_name = "taxon_form_wizard.html"
    file_storage = FileSystemStorage(location='/tmp')

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        data['status'] = False
        Taxon.objects.create(**data)
        messages.info(self.request, 'Seu cadastro será analisado por um administrador.')
        return HttpResponseRedirect(reverse('listar_especies'))

@method_decorator(never_cache, name='dispatch')
class EditTaxonWizard(SessionWizardView):
    form_list = [
        TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form,
        TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form,
        TaxonStep9Form
    ]
    template_name = "edit_taxon_wizard.html"
    file_storage = FileSystemStorage(location='/tmp')

    def get_wizard_kwargs(self, step):
        kwargs = super().get_wizard_kwargs(step)
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step)
        pk = self.kwargs.get('pk')
        if pk:
            taxon = get_object_or_404(Taxon, pk=pk)
            kwargs['instance'] = taxon
        return kwargs

    def done(self, form_list, **kwargs):
        updated = any(form.has_changed() for form in form_list)
        pk = self.kwargs.get('pk')
        taxon = get_object_or_404(Taxon, pk=pk)

        if updated:
            data = {}
            for form in form_list:
                data.update(form.cleaned_data)

            taxon.taxonID = data.get('taxonID')
            taxon.acceptedNameUsageID = data.get('acceptedNameUsageID')
            taxon.parentNameUsageID = data.get('parentNameUsageID')
            taxon.originalNameUsageID = data.get('originalNameUsageID')
            taxon.scientificName = data.get('scientificName')
            taxon.acceptedNameUsage = data.get('acceptedNameUsage')
            taxon.parentNameUsage = data.get('parentNameUsage')
            taxon.namePublishedIn = data.get('namePublishedIn')
            taxon.namePublishedInYear = data.get('namePublishedInYear')
            taxon.higherClassification = data.get('higherClassification')
            taxon.kingdom = data.get('kingdom')
            taxon.phylum = data.get('phylum')
            taxon.classe = data.get('classe')
            taxon.order = data.get('order')
            taxon.family = data.get('family')
            taxon.genus = data.get('genus')
            taxon.specificEpithet = data.get('specificEpithet')
            taxon.infraspecificEpithet = data.get('infraspecificEpithet')
            taxon.taxonRank = data.get('taxonRank')
            taxon.bibliographicCitation = data.get('bibliographicCitation')
            taxon.references = data.get('references')
            taxon.foto = data.get('foto')

            taxon.save()
            messages.success(self.request, 'Atualização realizada com sucesso.')
        else:
            messages.info(self.request, 'Nenhuma mudança detectada.')

        return render(self.request, self.template_name, {
            'done': True,
            'taxon': taxon
        })

def history_Taxon(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    historico = taxon.history.all().order_by('history_date')
    historico_detalhado = []
    anterior = None

    for item in historico:
        diffs = []
        if anterior:
            delta = anterior.diff_against(item)
            for change in delta.changes:
                if change.field == 'status':
                    continue
                diffs.append({
                    'field': change.field,
                    'old': change.old,
                    'new': change.new,
                })

        historico_detalhado.append({
            'data': item.history_date,
            'tipo': item.history_type,
            'objeto': item,
            'diferencas': diffs,
            'usuario': item.history_user,
        })
        anterior = item

    historico_detalhado.reverse()

    return render(request, 'history_taxon.html', {
        'taxon': taxon,
        'historico': historico_detalhado
    })
