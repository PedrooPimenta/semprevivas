from django.contrib import admin

# Register your models here.
from .models import Taxon  # Substitua "Perfil" pelo nome do seu modelo

admin.site.register(Taxon)