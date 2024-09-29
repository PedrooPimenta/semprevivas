from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.
class Taxon(models.Model):
    # numero da taxonomia
    taxonID = models.IntegerField(verbose_name="ID na Taxonomia")
    # ID do nome aceito 
    acceptedNameUsageID = models.IntegerField(verbose_name="ID do Nome Aceito",blank=True,null=True)
    parentNameUsageID = models.IntegerField(blank=True,null=True)
    originalNameUsageID = models.IntegerField(blank=True,null=True)
    scientificName = models.CharField(max_length=255,blank=True,null=True)
    acceptedNameUsage = models.CharField(max_length=255,blank=True,null=True)
    parentNameUsage = models.CharField(max_length=255,blank=True,null=True)
    namePublishedIn = models.CharField(max_length=255,blank=True,null=True)
    namePublishedInYear = models.IntegerField(blank=True,null=True)
    higherClassification = models.CharField(max_length=255,blank=True,null=True)
    kingdom = models.CharField(max_length=255,blank=True,null=True)
    phylum = models.CharField(max_length=255,blank=True,null=True)
    classe = models.CharField(max_length=255,blank=True,null=True)  # Usar db_column para evitar conflito com a palavra reservada 'class' do Python
    order = models.CharField(max_length=255,blank=True,null=True)
    family = models.CharField(max_length=255,blank=True,null=True)
    genus = models.CharField(max_length=255,blank=True,null=True)
    specificEpithet = models.CharField(max_length=255,blank=True,null=True)
    infraspecificEpithet = models.CharField(max_length=255,blank=True,null=True)
    taxonRank = models.CharField(max_length=255,blank=True,null=True)
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
    modified = models.DateTimeField()
    bibliographicCitation = models.TextField(blank=True,null=True)
    references = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.scientificName