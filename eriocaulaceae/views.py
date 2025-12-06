import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin

import pandas as pd
import ast
from .forms import (
    TaxonForm, CSVUploadForm,
    TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form,
    TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form, TaxonStep9Form
)
from .models import Taxon
from django.views.generic.detail import DetailView


class dados_especies(DetailView):
    model = Taxon
    template_name = 'dados_da_especie.html'
    context_object_name = 'especie'

    def get_queryset(self):
        return Taxon.objects.filter(status=True).order_by('scientificName')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        especie = self.get_object()
        context['form'] = TaxonForm(instance=especie)
        return context    

def eriocaulaceae_home(request):
    return render(request, "eriocaulaceae_home.html")


@login_required
def eriocaulaceae_adicionar(request):
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
    queryset = Taxon.objects.filter(status=True).order_by('created_at')
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
            try:
                valores = taxon.estado
                if isinstance(valores, str):
                    siglas = ast.literal_eval(valores)
                else:
                    siglas = valores
                nomes_completos = [estados.get(sigla, sigla)
                                   for sigla in siglas]
                taxon.estado = nomes_completos
            except Exception:
                taxon.estado = None
        else:
            taxon.estado = None
    context = {
        'page_obj': page_obj,
        'termo_busca': termo_busca,
        'solicitacoes_pendentes': solicitacoes_pendentes
    }
    return render(request, 'listar_especies.html', context)


@login_required
def minhas_especies_cadastradas(request):
    # não permitir acesso para usuários no grupo 'Convidado'
    if request.user.groups.filter(name='Convidado').exists():
        return render(request, 'access_denied.html', status=403)
    """Lista as espécies que o usuário criou (entradas de criação no histórico)."""
    usuario = request.user
    HistModel = Taxon.history.model
    created_qs = HistModel.objects.filter(
        history_user=usuario, history_type='+').values_list('id', flat=True).distinct()
    taxa_qs = Taxon.objects.filter(
        id__in=list(created_qs)).order_by('-created_at')
    paginator = Paginator(taxa_qs, 10)
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
            try:
                valores = taxon.estado
                if isinstance(valores, str):
                    siglas = ast.literal_eval(valores)
                else:
                    siglas = valores
                nomes_completos = [estados.get(sigla, sigla)
                                   for sigla in siglas]
                taxon.estado = nomes_completos
            except Exception:
                taxon.estado = None
        else:
            taxon.estado = None

    return render(request, 'minhas_especies.html', {'page_obj': page_obj})


@login_required
def buscar_especies(request):
    especies = []
    termo_busca = 'Erio'
    if request.method == 'POST':
        termo_busca = request.POST.get('termo_busca')
        especies = Taxon.objects.filter(
            Q(scientificName__icontains=termo_busca) |
            Q(acceptedNameUsage__icontains=termo_busca)
        )
    return render(request, 'buscar_especies.html', {'especies': especies, 'termo_busca': termo_busca})


@login_required
def editar_especie(request, especie_id):
    especie = get_object_or_404(Taxon, id=especie_id)
    if request.method == 'POST':
        form = TaxonForm(request.POST, instance=especie)
        if form.is_valid():
            especie = form.save(commit=False)
            especie.status = False
            especie.tipo_solicitacao = 'edicao'
            especie.save()
            messages.info(
                request, 'Edição enviada para análise do administrador.')
            return redirect('listar_especies')
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
def toggle_status(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    # Se for uma solicitação de exclusão e o admin aprovar (status passa de False -> aprovar),
    # devemos remover o objeto (aprovação da exclusão). Caso contrário apenas alternar o status.
    if taxon.tipo_solicitacao == 'exclusao' and taxon.status is False:
        # aprovar exclusão: deletar
        taxon.delete()
        messages.info(request, 'Exclusão aprovada. Espécie removida.')
    else:
        taxon.status = not taxon.status
        # se estamos aprovando (status True) removemos o tipo_solicitacao
        if taxon.status:
            taxon.tipo_solicitacao = None
        taxon.save()
        messages.info(request, 'Status atualizado.')
    return redirect('listar_solicitacoes')


@login_required
def list_solicitacoes(request):
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)

    solicitacoes = Taxon.objects.filter(status=False).order_by('created_at')
    solicitacoes_detalhadas = []

    for s in solicitacoes:
        diferencas = []
        usuario_solicitacao = None

        # busca histórico do objeto (mais recente primeiro) e tenta localizar o usuário
        historico_desc = s.history.order_by('-history_date')

        # Para edições, coletar as diferenças entre último e anterior
        if s.tipo_solicitacao == 'edicao':
            historico = historico_desc
            if historico.count() >= 2:
                ultima = historico[0]
                anterior = historico[1]
                delta = ultima.diff_against(anterior)
                for change in delta.changes:
                    if change.field in ['status', 'tipo_solicitacao']:
                        continue
                    diferencas.append({
                        'field': change.field,
                        'old': change.old,
                        'new': change.new
                    })

        # tenta encontrar no histórico um entry cujo campo tipo_solicitacao corresponda
        # ao tipo atual e que tenha history_user informado
        historico_all = s.history.order_by('-history_date')
        for h in historico_all:
            if getattr(h, 'history_user', None) is None:
                continue
            if getattr(h, 'tipo_solicitacao', None) == s.tipo_solicitacao:
                usuario_solicitacao = getattr(h, 'history_user')
                break

        # se não encontrou correspondência por tipo, pega primeiro history_user não nulo
        if usuario_solicitacao is None:
            for h in historico_all:
                if getattr(h, 'history_user', None):
                    usuario_solicitacao = getattr(h, 'history_user')
                    break

        solicitacoes_detalhadas.append({
            'objeto': s,
            'diferencas': diferencas,
            'usuario': usuario_solicitacao
        })

    return render(request, 'list_solicitacoes.html', {
        'solicitacoes': solicitacoes_detalhadas
    })


@login_required
def minhas_solicitacoes(request):
    if request.user.groups.filter(name='Convidado').exists():
        return render(request, 'access_denied.html', status=403)
    """Mostra para o pesquisador as solicitações que ele fez e o status de cada uma.

    Critérios usados:
    - Filtra apenas o histórico do usuário atual no banco de dados (otimizado).
    - Para cada histórico cria um registro com: taxon, tipo_solicitacao (cadastro/edicao/exclusao), data, e status atual do objeto (Aprovado/Negado/Pendente).
    """
    usuario = request.user
    resultados = []
    
    HistModel = Taxon.history.model
    user_history = HistModel.objects.filter(history_user=usuario).order_by('id', 'history_date')
    
    from django.db.models import Q
    taxon_ids = user_history.values_list('id', flat=True).distinct()
    taxons = {t.id: t for t in Taxon.objects.filter(id__in=taxon_ids)}
    
    history_cache = {}
    for taxon_id in taxon_ids:
        history_cache[taxon_id] = list(
            HistModel.objects.filter(id=taxon_id).order_by('history_date')
        )
    
    from types import SimpleNamespace

    for hist_entry in user_history:
        taxon_id = hist_entry.id
        taxon = taxons.get(taxon_id)
        history = history_cache.get(taxon_id, [])

        if taxon is None:
            taxon = SimpleNamespace(
                scientificName=getattr(hist_entry, 'scientificName', '-') ,
                pk=taxon_id,
                status=getattr(hist_entry, 'status', None),
                tipo_solicitacao=getattr(hist_entry, 'tipo_solicitacao', None),
                _deleted=True
            )
        
        event_idx = None
        for idx, h in enumerate(history):
            if h.history_id == hist_entry.history_id:
                event_idx = idx
                break
        
        if event_idx is None:
            continue
        
        event = history[event_idx]
        prev = history[event_idx - 1] if event_idx > 0 else None
        
        admin_event = None
        for j in range(event_idx + 1, len(history)):
            if getattr(history[j], 'history_user', None) != usuario:
                admin_event = history[j]
                break
        
        tipo = getattr(event, 'tipo_solicitacao', None) or getattr(taxon, 'tipo_solicitacao', None)

        status_text = 'Pendente'
        if tipo == 'exclusao':
            if admin_event:
                if getattr(admin_event, 'history_type', None) == '-':
                    status_text = 'Aprovado'
                else:
                    if getattr(admin_event, 'status', None) is True:
                        status_text = 'Negado'
                    elif getattr(admin_event, 'status', None) is False:
                        status_text = 'Aprovado'
                    else:
                        status_text = 'Negado'
            else:
                if getattr(taxon, '_deleted', False):
                    status_text = 'Aprovado'
                elif getattr(taxon, 'status', None) is False and getattr(taxon, 'tipo_solicitacao', None):
                    status_text = 'Pendente'
                else:
                    status_text = 'Negado'
        else:
            if admin_event:
                if getattr(admin_event, 'history_type', None) == '-':
                    status_text = 'Negado'
                else:
                    admin_status = getattr(admin_event, 'status', None)
                    if admin_status is True:
                        status_text = 'Aprovado'
                    elif admin_status is False:
                        status_text = 'Negado'
                    else:
                        status_text = 'Aprovado'
            else:
                if getattr(taxon, 'status', None) is True and not getattr(taxon, 'tipo_solicitacao', None):
                    status_text = 'Aprovado'
                elif getattr(taxon, 'status', None) is False and getattr(taxon, 'tipo_solicitacao', None):
                    status_text = 'Pendente'
                else:
                    status_text = 'Negado'
        
        resultados.append({
            'taxon': taxon,
            'evento': event,
            'tipo_solicitacao': tipo,
            'data': event.history_date,
            'status_text': status_text,
            'link_historico': reverse('historico_taxon', args=[taxon.pk])
        })

    resultados.sort(key=lambda x: x['data'] or datetime.datetime.min, reverse=True)

    return render(request, 'minhas_solicitacoes.html', {
        'resultados': resultados
    })


@login_required
def negar_edicao(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    if taxon.tipo_solicitacao == 'edicao':
        taxon.status = True
        taxon.tipo_solicitacao = 'cadastro'
        taxon.save()
        messages.info(request, 'Edição negada. Versão anterior mantida.')
    return redirect('listar_solicitacoes')


@login_required
def adicionar_especie(request):
    if request.method == 'POST':
        form = TaxonForm(request.POST)
        if form.is_valid():
            taxon_obj = form.save(commit=False)
            taxon_obj.status = False
            taxon_obj.tipo_solicitacao = 'cadastro'
            taxon_obj.save()
            messages.info(
                request, 'Cadastro enviado para análise do administrador.')
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
                        references=linha['references'],
                        endemismo=linha['endemismo'],
                        conservacao=linha['conservacao'],
                        conservacao_fonte=linha['conservacao_fonte'],
                        caule=linha['caule'],
                    )
                    taxon.save()
                return render(request, 'sucesso.html')
            else:
                return render(request, 'erro.html', {'mensagem': 'O arquivo enviado não é um arquivo CSV.'})
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


class TaxonWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [
        TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form,
        TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form,
        TaxonStep9Form
    ]
    template_name = "taxon_form_wizard.html"
    file_storage = FileSystemStorage(location='/tmp')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
            return render(request, 'access_denied.html', status=403)
        return super().dispatch(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
            scientific_name = data.get("scientificName")

        if Taxon.objects.filter(scientificName__iexact=scientific_name).exists():
            messages.error(self.request, "Já existe uma espécie cadastrada com este nome científico.")
            return HttpResponseRedirect(reverse('adicionar_taxon'))
        
        data['status'] = False
        data['tipo_solicitacao'] = 'cadastro'
        data['user'] = self.request.user
        Taxon.objects.create(**data)
        messages.info(
            self.request, 'Cadastro enviado para análise do administrador.')
        return HttpResponseRedirect(reverse('listar_especies'))
        



@method_decorator(never_cache, name='dispatch')
class EditTaxonWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [
        TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form,
        TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form,
        TaxonStep9Form
    ]
    template_name = "edit_taxon_wizard.html"
    file_storage = FileSystemStorage(location='/tmp')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "access_denied.html", {"message": "Você precisa estar logado."}, status=401)
        if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
            return render(request, "access_denied.html", {"message": "Você não tem permissão para editar espécies."}, status=403)
        return super().dispatch(request, *args, **kwargs)

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
            taxon.descricao_morfologica = data.get('descricao_morfologica')
            taxon.chave_identificacao = data.get('chave_identificacao')
            taxon.comentarios = data.get('comentarios')

            taxon.references = data.get('references')
            
            taxon.estado = data.get('estado')
            taxon.paises = data.get('paises')
            taxon.distribuicao_biomas = data.get('distribuicao_biomas')
            taxon.fitofisionomias = data.get('fitofisionomias')
            taxon.distribuicoes_formacoes = data.get('distribuicoes_formacoes')
            taxon.endemismo = data.get('endemismo')
            taxon.conservacao = data.get('conservacao')
            taxon.conservacao_fonte = data.get('conservacao_fonte')
            taxon.caule = data.get('caule')
            taxon.scientificNameAuthorship = data.get('scientificNameAuthorship')
            taxon.taxonomicStatus = data.get('taxonomicStatus')
            taxon.nomenclaturalStatus = data.get('nomenclaturalStatus')
            taxon.bibliographicCitation = data.get('bibliographicCitation')
            

            taxon.foto = data.get('foto')
            taxon.foto2 = data.get('foto2')
            taxon.foto3 = data.get('foto3')
            taxon.foto4 = data.get('foto4')
            taxon.foto5 = data.get('foto5')
            taxon.foto6 = data.get('foto6')
            taxon.foto7 = data.get('foto7')
            taxon.foto8 = data.get('foto8')
            taxon.localidade_das_fotos = data.get('localidade_das_fotos')

            taxon.localidade_das_fotos = data.get('localidade_das_fotos')

            taxon.status = False
            taxon.tipo_solicitacao = 'edicao'
            taxon.save()
            messages.info(
                self.request, 'Edição enviada para análise do administrador.')
        else:
            messages.info(self.request, 'Nenhuma mudança detectada.')
        return HttpResponseRedirect(reverse('listar_especies'))


@login_required
def history_Taxon(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    historico = taxon.history.all().order_by('history_date')
    historico_detalhado = []
    anterior = None

    for item in historico:
        if hasattr(item, 'status') and item.status is False:
            continue

        diffs = []
        if anterior:
            delta = item.diff_against(anterior)
            for change in delta.changes:
                if change.field in ['status', 'tipo_solicitacao']:
                    continue
                diffs.append({
                    'field': change.field,
                    'old': change.old,
                    'new': change.new,
                })

        if diffs:
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


@login_required
def toggle_status(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)

    if taxon.tipo_solicitacao == 'exclusao':
        taxon.delete()
        messages.success(request, 'Espécie excluída com sucesso.')
        return redirect('listar_solicitacoes')

    taxon.status = True
    taxon.tipo_solicitacao = None
    taxon.save()
    messages.success(request, 'Solicitação aprovada com sucesso.')

    return redirect('listar_solicitacoes')


@login_required
def negar_edicao(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)

    historico = taxon.history.order_by('-history_date')

    if historico.count() >= 2:
        estado_anterior = historico[1]

        for field in taxon._meta.get_fields():
            if field.name in ['id', 'pk', 'status']:
                continue
            if hasattr(estado_anterior, field.name):
                setattr(taxon, field.name, getattr(
                    estado_anterior, field.name))

        taxon.status = True
        taxon.save()

        messages.info(
            request, 'Edição negada e dados revertidos ao estado anterior.')
    else:
        messages.warning(request, 'Não há edição anterior para reverter.')

    return redirect('listar_especies')


@login_required
def set_especie_false(request, especie_id):
    especie = get_object_or_404(Taxon, id=especie_id)
    if request.method == 'POST':
        especie.tipo_solicitacao = 'exclusao'
        especie.status = False
        especie.save()
        return redirect('listar_especies')
    return render(request, 'apagar_especie.html', {'especie': especie})


@login_required
def negar_exclusao(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    if not request.user.groups.filter(name__in=['Adm', 'Pesquisadores']).exists():
        return render(request, 'access_denied.html', status=403)
    taxon.tipo_solicitacao = None
    taxon.status = True
    taxon.save()

    messages.info(request, 'Solicitação de exclusão negada. A espécie permanece ativa.')
    return redirect('listar_solicitacoes')

