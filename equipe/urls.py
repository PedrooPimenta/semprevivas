from django.urls import path
from . import views

urlpatterns =[
    path('',views.listar_equipe, name='listar_equipe'),
    path('adicionar_pesquisador/',views.adicionar_pesquisador,name='adicionar_pesquisador'),
    path('editar_pesquisador/<int:pesquisador_id>/', views.editar_pesquisador, name='editar_pesquisador'),
    path('apagar_pesquisador/<int:pesquisador_id>/', views.apagar_pesquisador, name='apagar_pesquisador'),
 ]
