from django.db import models
from multiselectfield import MultiSelectField

class Estado(models.Model):
    SIGLA_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    sigla = models.CharField(max_length=50, choices=SIGLA_CHOICES)

    def __str__(self):
        return self.get_sigla_display()


# Create your models here.
class Taxon(models.Model):
    # numero da taxonomia
    taxonID = models.IntegerField(verbose_name="ID na Taxonomia")
    # ID do nome aceito 
    acceptedNameUsageID = models.IntegerField(verbose_name="ID do Nome Aceito",blank=True,null=True)
    # parentNameUsageID
    parentNameUsageID = models.IntegerField(blank=True,null=True)
    # originalNameUsageID
    originalNameUsageID = models.IntegerField(blank=True,null=True)
    # nome científico
    scientificName = models.CharField(max_length=255,blank=True,null=True)
    # nome aceito
    acceptedNameUsage = models.CharField(max_length=255,blank=True,null=True)
    # parent name usage
    parentNameUsage = models.CharField(max_length=255,blank=True,null=True)
    # nome publicado
    namePublishedIn = models.CharField(max_length=255,blank=True,null=True)
    # ano de publicação
    namePublishedInYear = models.IntegerField(blank=True,null=True)
    # higherClassification
    higherClassification = models.CharField(max_length=255,blank=True,null=True)
    # kingdon
    kingdom = models.CharField(max_length=255,blank=True,null=True)
    #phylum
    phylum = models.CharField(max_length=255,blank=True,null=True)
    # classe
    classe = models.CharField(max_length=255,blank=True,null=True)  # Usar db_column para evitar conflito com a palavra reservada 'class' do Python
    #order
    order = models.CharField(max_length=255,blank=True,null=True)
    # family
    family = models.CharField(max_length=255,blank=True,null=True)
    # genus
    genus = models.CharField(max_length=255,blank=True,null=True)
    # specificEpithet
    specificEpithet = models.CharField(max_length=255,blank=True,null=True)
    # infraspecificEpithet
    infraspecificEpithet = models.CharField(max_length=255,blank=True,null=True)
    # taxonRank
    taxonRank = models.CharField(max_length=255,blank=True,null=True)

    #Descrição morfológica (para gêneros, e para as espécies de cada gênero): espaço para incluir um breve texto (descrição livre)
    descricao_morfologica = models.TextField(verbose_name="Descrição Morfológica", null=True, blank=True)

    # chave de identificação : (para gêneros, e para as espécies de cada gênero): espaço para incluir texto.
    chave_identificacao = models.TextField(verbose_name="Chave de Identificação", null=True, blank=True)

    # observações e comentários
    comentarios = models.TextField(verbose_name="Comentários", null=True, blank=True)

    # estado de ocorrência
    estado = models.TextField(null=True, blank=True)  # Campo de texto para armazenar JSON
    # paises de ocorrência
    paises = models.TextField(null=True, blank=True)  # Campo de texto para armazenar JSON
    # Distribuição (biomas brasileiros)
    distribuicao_biomas =models.TextField(null=True, blank=True)
    

    fitofisionomias = models.TextField(null=True, blank=True)


    distribuicoes_formacoes = models.TextField(null=True, blank=True)
    

    ENDEMISMO= (
        ('ALGUM_PAIS', 'Endêmica de algum país'),
        ('ALGUM_ESTADO', 'Endêmica (de algum ou alguns estados)'),
        ('BIOMAS', 'Endêmica de (biomas)'),
        ('FITOFISIONOMIAS', 'Endêmica de (fitofisionomias)'),
        ('SERRA', 'Endêmica de (alguma serra, formação geológica etc..)'),
    )
    endemismo= models.CharField(choices=ENDEMISMO, max_length=1000, null=True, blank=True)
    #endemismo = MultiSelectField(choices=ENDEMISMO, max_choices=100, max_length=1000, null=True, blank=True)

    CONSERVACAO=(
        ("EXTINTA", 'Extinta'),
        ("EXTINTA_NATUREZA", 'Extinta na natureza'),
        ('CRITICAMENTE_PERIGO', 'Criticamente em Perigo'),
        ('PERIGO', 'Em Perigo'),
        ('VULNERAVEL','Vulnerável'),
        ('QUASE_AMEACADA','Quase ameaçada'),
        ('MENOS_PREOCUPAMENTE', 'Menos preocupante'),
        ('NAO_AVALIADA','Não avaliada quanto ao grau de ameaça'),
        ('INSUFICIENTES','Dados Insuficientes'),
        ('NAO_AMEACADA', 'Não ameaçada'),    
    )
    conservacao= models.CharField(choices=CONSERVACAO, max_length=1000, null=True, blank=True)
    conservacao_fonte = models.TextField(verbose_name="Fonte de Onde foi retirada a Informação da Conservação",blank=True, null=True)

    
    CURTO = 'curto'
    ALONGADO = 'alongado'
    AEREO = 'aereo'
    ND = 'ND'

    CAULE_CHOICES = [
        (CURTO, 'Curto'),
        (ALONGADO, 'Alongado'),
        (AEREO, 'Aéreo'),
        (ND, 'Não determinado'),
    ]

    caule = models.CharField(max_length=50, choices=CAULE_CHOICES,blank=True,null=True)
    #caule1 = MultiSelectField(choices=CAULE_CHOICES,max_choices=3, max_length=50,blank=True,null=True)
    scientificNameAuthorship = models.CharField(max_length=255,blank=True,null=True)
    taxonomicStatus = models.CharField(max_length=255,blank=True,null=True)
    nomenclaturalStatus = models.CharField(max_length=255,blank=True,null=True)
    # campo que indica quando o registro foi modificado
    modified = models.DateTimeField(auto_now=True)
    # citações bibliográficas
    bibliographicCitation = models.TextField(blank=True,null=True,verbose_name="Referências Bibliográficas")
    # referências
    references = models.TextField(blank=True,null=True,verbose_name="Outras Referências")

    # imagem 
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)


    def __str__(self):
        return self.scientificName