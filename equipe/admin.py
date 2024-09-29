from django.contrib import admin

# Register your models here.
from .models import Pesquisador  # Substitua "Perfil" pelo nome do seu modelo

admin.site.register(Pesquisador)
