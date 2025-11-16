from django.urls import path
from . import views
from .forms import TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form, TaxonStep6Form, TaxonStep7Form, TaxonStep8Form, TaxonStep9Form

urlpatterns = [
    path('', views.eriocaulaceae_home, name='eriocaulaceae_home'),
    path('adicionar/', views.eriocaulaceae_adicionar,
         name='eriocaulaceae_adicionar'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('listar/', views.listar_especies, name='listar_especies'),
    path('minhas-especies/', views.minhas_especies_cadastradas,
         name='minhas_especies'),
    path('buscar_especies/', views.buscar_especies, name='buscar_especies'),
    path('editar-especie/<uuid:especie_id>/',
         views.editar_especie, name='editar_especie'),
    path('apagar-especie/<uuid:especie_id>/',
         views.apagar_especie, name='apagar_especie'),
    path('adicionar-especie/', views.adicionar_especie, name='adicionar_especie'),
    path("adicionar-taxon/", views.TaxonWizard.as_view([
        TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form,
        TaxonStep6Form, TaxonStep7Form, TaxonStep8Form, TaxonStep9Form
    ]), name="adicionar_taxon"),
    path("editar-taxon/<uuid:pk>/", views.EditTaxonWizard.as_view([
        TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form,
        TaxonStep6Form, TaxonStep7Form, TaxonStep8Form, TaxonStep9Form
    ]), name="editar_taxon"),
    path("taxon/<uuid:pk>/", views.history_Taxon, name="historico_taxon"),
    path('listar_solicitacoes/', views.list_solicitacoes,
         name='listar_solicitacoes'),
    path('minhas_solicitacoes/', views.minhas_solicitacoes,
         name='minhas_solicitacoes'),
    path('taxon/<uuid:pk>/toggle_status/',
         views.toggle_status, name='toggle_status'),
    path('set-especie/<uuid:especie_id>/',
         views.set_especie_false, name='set_especie_false'),
    path('taxon/<uuid:pk>/negar_edicao/',
         views.negar_edicao, name='negar_edicao'),
    path('negar_exclusao/<uuid:pk>/', views.negar_exclusao, name='negar_exclusao'),

]
