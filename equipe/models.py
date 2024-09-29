from django.db import models
from datetime import datetime

class Titulacao(models.TextChoices):
    GRADUANDO = "Graduando"
    GRADUACAO = "Graduação"
    MESTRADO = "Mestrado"
    DOUTORADO = "Doutorado"

class Pesquisador(models.Model):
    # nome do pesquisador 
    nome = models.CharField(max_length=255,verbose_name="Nome do Pesquisador")
    # titulacao 
    nivel = models.CharField(max_length=10, choices=Titulacao.choices, verbose_name="Titulação")
    # Link do Lattes
    lattes = models.URLField(blank=True, null=True, verbose_name="Lattes")
    # Link do Linkedin 
    linkedin = models.URLField(blank=True, null=True, verbose_name="Linkedin")
    # Link do Research Gate 
    researchgate = models.URLField(blank=True, null=True, verbose_name="Research Gate")
    # Email 
    email = models.EmailField(verbose_name="E-mail")
    # Data de criação do Perfil 
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    # ativo
    ativo = models.BooleanField(default=False)
    
    # cargo na instituição
    CARGO = {
    "ALUNO": "Aluno",
    "PROFESSOR": "Professor",
    "TECNICO": "Técnico",
    }

    # cargo na instituição
    cargo = models.CharField(max_length=10, choices=CARGO, verbose_name="Cargo")
    
    def __str__(self):
        return f"{self.nome} ({self.nivel})"
