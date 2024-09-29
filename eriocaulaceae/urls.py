from django.urls import path
from . import views

urlpatterns =[
    path('',views.eriocaulaceae_home, name='eriocaulaceae_home'),
    path('adicionar/', views.eriocaulaceae_adicionar, name='eriocaulaceae_adicionar'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('listar/', views.listar_especies, name='listar_especies'),
    path('buscar_especies/', views.buscar_especies, name='buscar_especies'),
    path('editar-especie/<int:especie_id>/', views.editar_especie, name='editar_especie'), 
    path('apagar-especie/<int:especie_id>/', views.apagar_especie, name='apagar_especie'),
    path('adicionar-especie/', views.adicionar_especie, name='adicionar_especie'),
    ]
