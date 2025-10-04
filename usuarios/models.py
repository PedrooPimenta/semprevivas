from django.contrib.auth.models import AbstractUser
from django.db import models

class Titulacao(models.TextChoices):
    GRADUANDO = "Graduando", "Graduando"
    GRADUACAO = "Graduação", "Graduação"
    MESTRADO = "Mestrado", "Mestrado"
    DOUTORADO = "Doutorado", "Doutorado"

class CustomUser(AbstractUser):
    nivel = models.CharField(max_length=20, choices=Titulacao.choices, verbose_name="Titulação", blank=True, null=True)
    lattes = models.URLField(blank=True, null=True, verbose_name="Lattes")
    linkedin = models.URLField(blank=True, null=True, verbose_name="Linkedin")
    researchgate = models.URLField(blank=True, null=True, verbose_name="Research Gate")
    email = models.EmailField("E-mail", unique=True)


    def __str__(self):
        return self.username
