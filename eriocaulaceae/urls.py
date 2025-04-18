from django.urls import path
from . import views
from .forms import TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form,TaxonStep6Form,TaxonStep7Form,TaxonStep8Form,TaxonStep9Form

urlpatterns =[
    path('',views.eriocaulaceae_home, name='eriocaulaceae_home'),
    path('adicionar/', views.eriocaulaceae_adicionar, name='eriocaulaceae_adicionar'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('listar/', views.listar_especies, name='listar_especies'),
    path('buscar_especies/', views.buscar_especies, name='buscar_especies'),
    path('editar-especie/<int:especie_id>/', views.editar_especie, name='editar_especie'), 
    path('apagar-especie/<int:especie_id>/', views.apagar_especie, name='apagar_especie'),
    path('adicionar-especie/', views.adicionar_especie, name='adicionar_especie'),
     path("adicionar-taxon/", views.TaxonWizard.as_view(
        [TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form,TaxonStep6Form,TaxonStep7Form,TaxonStep8Form,TaxonStep9Form]
    ), name="adicionar_taxon"),
    path("editar-taxon/<int:pk>/", views.EditTaxonWizard.as_view(
        [TaxonStep1Form, TaxonStep2Form, TaxonStep3Form, TaxonStep4Form, TaxonStep5Form,TaxonStep6Form,TaxonStep7Form,TaxonStep8Form,TaxonStep9Form]
    ), name="editar_taxon"),
    path("taxon/<int:pk>/", views.history_Taxon, name="historico_taxon"),
    path('listar_solicitacoes/', views.list_solicitacoes, name='listar_solicitacoes'),
    path('taxon/<int:pk>/toggle_status/', views.toggle_status, name='toggle_status'),
    path('set-especie/<int:especie_id>/', views.set_especie_false, name='set_especie_false'),
    
    ]
