from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.apps import AppConfig
from django.dispatch import receiver

@receiver(post_migrate)
def criar_grupos_padrao(sender, **kwargs):
    grupos = ["Adm", "Users"]
    for nome in grupos:
        group, criado = Group.objects.get_or_create(name=nome.strip())
    