from django import forms
from .models import Taxon
import json


class TaxonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define as opções de estados
        self.fields['estado'] = forms.MultipleChoiceField(
            choices=(
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
                        # Adicione mais estados conforme necessário
                   ),
            required=False,
            widget=forms.CheckboxSelectMultiple
        )
        self.fields['paises'] = forms.MultipleChoiceField(
            choices=(
                    # south america
                    ('AR', 'Argentina'),
                    ('BO', 'Bolívia'),
                    ('BR', 'Brasil'),
                    ('CL', 'Chile'),
                    ('CO', 'Colômbia'),
                    ('EC', 'Equador'),
                    ('GY', 'Guiana'),
                    ('PE', 'Peru'),
                    ('PY', 'Paraguai'),
                    ('SR', 'Suriname'),
                    ('UY', 'Uruguai'),
                    ('VE', 'Venezuela'),
                    # central america
                    ('BZ', 'Belize'),
                    ('CR', 'Costa Rica'),
                    ('SV', 'El Salvador'),
                    ('GT', 'Guatemala'),
                    ('HN', 'Honduras'),
                    ('NI', 'Nicarágua'),
                    ('PA', 'Panamá'),
                    # america do norte
                    ('CA', 'Canadá'),
                    ('US', 'Estados Unidos'),
                    ('MX', 'México'),
                    # europe
                    ('AL', 'Albânia'),
                    ('AD', 'Andorra'),
                    ('AT', 'Áustria'),
                    ('BY', 'Belarus'),
                    ('BE', 'Bélgica'),
                    ('BA', 'Bósnia e Herzegovina'),
                    ('BG', 'Bulgária'),
                    ('HR', 'Croácia'),
                    ('CY', 'Chipre'),
                    ('CZ', 'República Tcheca'),
                    ('DK', 'Dinamarca'),
                    ('EE', 'Estônia'),
                    ('FI', 'Finlândia'),
                    ('FR', 'França'),
                    ('DE', 'Alemanha'),
                    ('GR', 'Grécia'),
                    ('HU', 'Hungria'),
                    ('IS', 'Islândia'),
                    ('IE', 'Irlanda'),
                    ('IT', 'Itália'),
                    ('LV', 'Letônia'),
                    ('LI', 'Liechtenstein'),
                    ('LT', 'Lituânia'),
                    ('LU', 'Luxemburgo'),
                    ('MK', 'Macedônia do Norte'),
                    ('MT', 'Malta'),
                    ('MD', 'Moldávia'),
                    ('MC', 'Mônaco'),
                    ('ME', 'Montenegro'),
                    ('NL', 'Países Baixos'),
                    ('NO', 'Noruega'),
                    ('PL', 'Polônia'),
                    ('PT', 'Portugal'),
                    ('RO', 'Romênia'),
                    ('RU', 'Rússia'),
                    ('SM', 'San Marino'),
                    ('RS', 'Sérvia'),
                    ('SK', 'Eslováquia'),
                    ('SI', 'Eslovênia'),
                    ('ES', 'Espanha'),
                    ('SE', 'Suécia'),
                    ('CH', 'Suíça'),
                    ('TR', 'Turquia'),
                    ('UA', 'Ucrânia'),
                    ('GB', 'Reino Unido'),
                    ('VA', 'Vaticano'),
                    # africa
                    ('DZ', 'Argélia'),
                    ('AO', 'Angola'),
                    ('BJ', 'Benin'),
                    ('BW', 'Botsuana'),
                    ('BF', 'Burkina Faso'),
                    ('BI', 'Burundi'),
                    ('CM', 'Camarões'),
                    ('CV', 'Cabo Verde'),
                    ('CF', 'República Centro-Africana'),
                    ('TD', 'Chade'),
                    ('KM', 'Comores'),
                    ('CG', 'República do Congo'),
                    ('CD', 'República Democrática do Congo'),
                    ('DJ', 'Djibuti'),
                    ('EG', 'Egito'),
                    ('GQ', 'Guiné Equatorial'),
                    ('ER', 'Eritreia'),
                    ('ET', 'Etiópia'),
                    ('GA', 'Gabão'),
                    ('GM', 'Gâmbia'),
                    ('GH', 'Gana'),
                    ('GN', 'Guiné'),
                    ('GW', 'Guiné-Bissau'),
                    ('CI', 'Costa do Marfim'),
                    ('KE', 'Quênia'),
                    ('LS', 'Lesoto'),
                    ('LR', 'Libéria'),
                    ('LY', 'Líbia'),
                    ('MG', 'Madagascar'),
                    ('MW', 'Malawi'),
                    ('ML', 'Mali'),
                    ('MR', 'Mauritânia'),
                    ('MU', 'Maurício'),
                    ('MA', 'Marrocos'),
                    ('MZ', 'Moçambique'),
                    ('NA', 'Namíbia'),
                    ('NE', 'Níger'),
                    ('NG', 'Nigéria'),
                    ('RW', 'Ruanda'),
                    ('ST', 'São Tomé e Príncipe'),
                    ('SN', 'Senegal'),
                    ('SC', 'Seychelles'),
                    ('SL', 'Serra Leoa'),
                    ('SO', 'Somália'),
                    ('ZA', 'África do Sul'),
                    ('SS', 'Sudão do Sul'),
                    ('SD', 'Sudão'),
                    ('SZ', 'Suazilândia'),
                    ('TZ', 'Tanzânia'),
                    ('TG', 'Togo'),
                    ('TN', 'Tunísia'),
                    ('UG', 'Uganda'),
                    ('ZM', 'Zâmbia'),
                    ('ZW', 'Zimbábue'),
                    # ASIA
                    ('AF', 'Afeganistão'),
                    ('AM', 'Armênia'),
                    ('AZ', 'Azerbaijão'),
                    ('BH', 'Bahrein'),
                    ('BD', 'Bangladesh'),
                    ('BT', 'Butão'),
                    ('BN', 'Brunei'),
                    ('KH', 'Camboja'),
                    ('CN', 'China'),
                    ('CY', 'Chipre'),
                    ('GE', 'Geórgia'),
                    ('IN', 'Índia'),
                    ('ID', 'Indonésia'),
                    ('IR', 'Irã'),
                    ('IQ', 'Iraque'),
                    ('IL', 'Israel'),
                    ('JP', 'Japão'),
                    ('JO', 'Jordânia'),
                    ('KZ', 'Cazaquistão'),
                    ('KW', 'Kuwait'),
                    ('KG', 'Quirguistão'),
                    ('LA', 'Laos'),
                    ('LB', 'Líbano'),
                    ('MY', 'Malásia'),
                    ('MV', 'Maldivas'),
                    ('MN', 'Mongólia'),
                    ('MM', 'Myanmar'),
                    ('NP', 'Nepal'),
                    ('KP', 'Coreia do Norte'),
                    ('OM', 'Omã'),
                    ('PK', 'Paquistão'),
                    ('PS', 'Territórios Palestinos'),
                    ('PH', 'Filipinas'),
                    ('QA', 'Catar'),
                    ('SA', 'Arábia Saudita'),
                    ('SG', 'Singapura'),
                    ('KR', 'Coreia do Sul'),
                    ('LK', 'Sri Lanka'),
                    ('SY', 'Síria'),
                    ('TW', 'Taiwan'),
                    ('TJ', 'Tajiquistão'),
                    ('TH', 'Tailândia'),
                    ('TL', 'Timor-Leste'),
                    ('TR', 'Turquia'),
                    ('TM', 'Turcomenistão'),
                    ('AE', 'Emirados Árabes Unidos'),
                    ('UZ', 'Uzbequistão'),
                    ('VN', 'Vietnã'),
                    ('YE', 'Iêmen'),
                    # oceania
                    ('AS', 'Samoa Americana'),
                    ('AU', 'Austrália'),
                    ('CK', 'Ilhas Cook'),
                    ('FJ', 'Fiji'),
                    ('PF', 'Polinésia Francesa'),
                    ('GU', 'Guam'),
                    ('KI', 'Kiribati'),
                    ('MH', 'Ilhas Marshall'),
                    ('FM', 'Micronésia'),
                    ('NR', 'Nauru'),
                    ('NC', 'Nova Caledônia'),
                    ('NZ', 'Nova Zelândia'),
                    ('NU', 'Niue'),
                    ('NF', 'Ilha Norfolk'),
                    ('MP', 'Ilhas Marianas do Norte'),
                    ('PW', 'Palau'),
                    ('PG', 'Papua Nova Guiné'),
                    ('PN', 'Pitcairn'),
                    ('WS', 'Samoa'),
                    ('SB', 'Ilhas Salomão'),
                    ('TK', 'Tokelau'),
                    ('TO', 'Tonga'),
                    ('TV', 'Tuvalu'),
                    ('VU', 'Vanuatu'),
                    ('WF', 'Wallis e Futuna'),
                ),
        required=False,
            widget=forms.CheckboxSelectMultiple
        )

        self.fields['distribuicao_biomas'] = forms.MultipleChoiceField(
            choices=(
                        ('CERRADO', 'Cerrado'),
                        ('AMAZONIA', 'Amazonia'),
                        ("CAATINGA", 'Caatinga'),
                        ("PANTANAL", 'Pantanal'),
                        ("PAMPA", 'Pampa'),
                        ('MATAATLANTICA', 'Mata Atlântica'),
                   ),
        required=False,
            widget=forms.CheckboxSelectMultiple
        )

        self.fields['fitofisionomias'] = forms.MultipleChoiceField(
            choices=(
                ('AREAANTROPICA', 'Área antrópica'),
                ('CAATINGA', 'Caatinga'),
                ('CAMPINARANA', 'Campinarana'),
                ('CAMPOLIMPOSECO', 'Campo limpo seco'),
                ('CAMPOLIMPOUMIDO', 'Campo limpo úmido'),
                ('TURFEIRA', 'Turfeira (peatland)'),
                ('CAMPODEALTITUDE', 'Campo de altitude'),
                ('CAMPODEVARZEA', 'Campo de várzea'),
                ('CAMPORUPESTREQUARTZITICO', 'Campo rupestre quartzítico'),
                ('CAMPORUPESTREFERRUGINOSO', 'Campo rupestre ferruginoso'),
                ('INSELBERG', 'Inselberg (granito/gnaisse)'),
                ('CARSTICAS', 'Feições cársticas'),
                ('CARRASCO', 'Carrasco'),
                ('CERRADAO', 'Cerradão'),
                ('CERRADOSTRICTOSENSU', 'Cerrado stricto sensu'),
                ('CAMPOSUJO', 'Campo Sujo'),
                ('FLORESTACILIAR', 'Floresta Ciliar e/ou de Galeria'),
                ('FLORESTADEIGAPO', 'Floresta de Igapó'),
                ('FLORESTADETERRAFIRME', 'Floresta de Terra-Firme'),
                ('FLORESTADEVARZEA', 'Floresta de Várzea'),
                ('FLORESTAESTACIONALDECIDUAL', 'Floresta Estacional Decidual'),
                ('FLORESTAESTACIONALPERENIFOLIA',
                 'Floresta Estacional Perenifólia'),
                ('FLORESTASEMIDECIDUAL', 'Floresta Semidecidual'),
                ('FLORESTAOMBROFILA', 'Floresta Ombrófila (Floresta Pluvial)'),
                ('FLORESTAOMBROFILAMISTA', 'Floresta Ombrófila Mista'),
                ('MANGUEZAL', 'Manguezal'),
                ('VEREDA', 'Vereda (buritizal)'),
                ('RESTINGA', 'Restinga'),
                ('SAVANA', 'Savana Amazônica'),
                ('VEGETACAOAQUATICA', 'Vegetação aquática'),
                ('EMAFLORAMENTOSROCHOSOSQUARTZITICOS',
                 'em afloramentos rochosos quartzíticos'),
                ('EMAFLORAMENTOSROCHOSOSGRANITICOS',
                 'em afloramentos rochosos graníticos'),
                ('EMAFLORAMENTOSFERRUGINOSOS',
                 'em afloramentos rochosos ferruginosos'),
                   ),
        required=False,
            widget=forms.CheckboxSelectMultiple
        )
        self.fields['distribuicoes_formacoes'] = forms.MultipleChoiceField(
            choices=(
                ('ESPINHACO', 'Serra do Espinhaço'),
                ('MANTIQUEIRA', 'Serra da Mantiqueira'),
                ('CANASTRA', 'Serra da Canastra'),
                ('CAPIVARA', 'Serra da Capivara'),
                ('DIAMANTINA', 'Chapada Diamantina'),
                ('VEADEIROS', 'Chapada dos Veadeiros'),
                ('GUIMARAES', 'Chapada dos Guimarães'),
                ('IBITIPOCA', 'Serra de Ibitipoca'),
                ('CABRAL', 'Serra do Cabral'),
                ('AMBROSIO', 'Serra do Ambrósio'),
                ('ANGELO', 'Serra do Padre Ângelo'),
                ('MAR', 'Serra do Mar'),
                ('SERRA', 'Aparados da Serra'),
                ('CARAJAS', 'Serra dos Carajás'),
                ('TPEQUEM', 'Serra de Tapequém (RR)'),
                ('CARACA', 'Serra do Caraça'),
                ('BOCAINA', 'Complexo de Serras da Bocaina'),
                ('ITATIAIA', 'Serra de Itatiaia'),
                ('CIPO', 'Serra do Cipó'),
                ('INTENTENDE', 'Serra do Intendente'),
                ('NEGRA', 'Serra Negra (Itamarandiba, MG)'),
                ('NOVA', 'Serra Nova (MG)'),
                ('RORAIMA', 'Monte Roraima'),
                ('NEBLINA', 'Pico da Neblina'),
                ),
        required=False,
            widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = Taxon
        fields = '__all__'  # Todos os campos do model

    def save(self, commit=True):
        instance = super().save(commit=False)
        estados_selecionados = self.cleaned_data.get('estados')
        paises_selecionados = self.cleaned_data.get('paises')
        distribuicao_biomas_selecionados = self.cleaned_data.get(
            'distribuicao_biomas')
        fitofisionomias_selecionados = self.cleaned_data.get('fitofisionomias')
        distribuicoes_formacoes_selecionados = self.cleaned_data.get(
            'distribuicoes_formacoes')

        if estados_selecionados:
            instance.estados = json.dumps(estados_selecionados)
        if paises_selecionados:
            instance.paises = json.dumps(paises_selecionados)
        if distribuicao_biomas_selecionados:
            instance.distribuicao_biomas = json.dumps(
                distribuicao_biomas_selecionados)
        if fitofisionomias_selecionados:
            instance.fitofisionomias = json.dumps(fitofisionomias_selecionados)

        if distribuicoes_formacoes_selecionados:
            instance.distribuicoes_formacoes = json.dumps(
                distribuicoes_formacoes_selecionados)

        if commit:
            instance.save()
        return instance


class CSVUploadForm(forms.Form):
    arquivo_csv = forms.FileField()


# step
class BaseTaxonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {'class': 'form-control rounded border p-2'})


class TaxonStep1Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['taxonID', 'acceptedNameUsageID',
            'parentNameUsageID', 'originalNameUsageID']
        widgets = {
            'taxonID': forms.TextInput(attrs={'placeholder': 'Digite o ID do táxon'}),
        }


class TaxonStep2Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['scientificName', 'acceptedNameUsage',
            'parentNameUsage', 'namePublishedIn', 'namePublishedInYear']

        error_messages = {
            'scientificName': {'required': 'O nome científico é obrigatório.'},
            'namePublishedInYear': {'invalid': 'Digite um ano válido (formato: YYYY).'},
        }


class TaxonStep3Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['higherClassification', 'kingdom',
            'phylum', 'classe', 'order', 'family', 'genus']


class TaxonStep4Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['specificEpithet', 'infraspecificEpithet',
            'taxonRank', 'descricao_morfologica', 'chave_identificacao']
        widgets = {
            'descricao_morfologica': forms.Textarea(attrs={'rows': 3}),
            'chave_identificacao': forms.Textarea(attrs={'rows': 3}),
        }


class TaxonStep5Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['bibliographicCitation', 'references', 'foto']
        widgets = {
            'references': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'] = forms.MultipleChoiceField(
            choices=[
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
            ],
            required=False,
            widget=forms.CheckboxSelectMultiple(
                attrs={'class': 'custom-checkbox rounded border p-2'})
        )


class TaxonStep6Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['paises']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paises']=forms.MultipleChoiceField(
            choices=(
                    # south america
                    ('AR', 'Argentina'),
                    ('BO', 'Bolívia'),
                    ('BR', 'Brasil'),
                    ('CL', 'Chile'),
                    ('CO', 'Colômbia'),
                    ('EC', 'Equador'),
                    ('GY', 'Guiana'),
                    ('PE', 'Peru'),
                    ('PY', 'Paraguai'),
                    ('SR', 'Suriname'),
                    ('UY', 'Uruguai'),
                    ('VE', 'Venezuela'),
                    # central america
                    ('BZ', 'Belize'),
                    ('CR', 'Costa Rica'),
                    ('SV', 'El Salvador'),
                    ('GT', 'Guatemala'),
                    ('HN', 'Honduras'),
                    ('NI', 'Nicarágua'),
                    ('PA', 'Panamá'),
                    # america do norte
                    ('CA', 'Canadá'),
                    ('US', 'Estados Unidos'),
                    ('MX', 'México'),
                    # europe
                    ('AL', 'Albânia'),
                    ('AD', 'Andorra'),
                    ('AT', 'Áustria'),
                    ('BY', 'Belarus'),
                    ('BE', 'Bélgica'),
                    ('BA', 'Bósnia e Herzegovina'),
                    ('BG', 'Bulgária'),
                    ('HR', 'Croácia'),
                    ('CY', 'Chipre'),
                    ('CZ', 'República Tcheca'),
                    ('DK', 'Dinamarca'),
                    ('EE', 'Estônia'),
                    ('FI', 'Finlândia'),
                    ('FR', 'França'),
                    ('DE', 'Alemanha'),
                    ('GR', 'Grécia'),
                    ('HU', 'Hungria'),
                    ('IS', 'Islândia'),
                    ('IE', 'Irlanda'),
                    ('IT', 'Itália'),
                    ('LV', 'Letônia'),
                    ('LI', 'Liechtenstein'),
                    ('LT', 'Lituânia'),
                    ('LU', 'Luxemburgo'),
                    ('MK', 'Macedônia do Norte'),
                    ('MT', 'Malta'),
                    ('MD', 'Moldávia'),
                    ('MC', 'Mônaco'),
                    ('ME', 'Montenegro'),
                    ('NL', 'Países Baixos'),
                    ('NO', 'Noruega'),
                    ('PL', 'Polônia'),
                    ('PT', 'Portugal'),
                    ('RO', 'Romênia'),
                    ('RU', 'Rússia'),
                    ('SM', 'San Marino'),
                    ('RS', 'Sérvia'),
                    ('SK', 'Eslováquia'),
                    ('SI', 'Eslovênia'),
                    ('ES', 'Espanha'),
                    ('SE', 'Suécia'),
                    ('CH', 'Suíça'),
                    ('TR', 'Turquia'),
                    ('UA', 'Ucrânia'),
                    ('GB', 'Reino Unido'),
                    ('VA', 'Vaticano'),
                    # africa
                    ('DZ', 'Argélia'),
                    ('AO', 'Angola'),
                    ('BJ', 'Benin'),
                    ('BW', 'Botsuana'),
                    ('BF', 'Burkina Faso'),
                    ('BI', 'Burundi'),
                    ('CM', 'Camarões'),
                    ('CV', 'Cabo Verde'),
                    ('CF', 'República Centro-Africana'),
                    ('TD', 'Chade'),
                    ('KM', 'Comores'),
                    ('CG', 'República do Congo'),
                    ('CD', 'República Democrática do Congo'),
                    ('DJ', 'Djibuti'),
                    ('EG', 'Egito'),
                    ('GQ', 'Guiné Equatorial'),
                    ('ER', 'Eritreia'),
                    ('ET', 'Etiópia'),
                    ('GA', 'Gabão'),
                    ('GM', 'Gâmbia'),
                    ('GH', 'Gana'),
                    ('GN', 'Guiné'),
                    ('GW', 'Guiné-Bissau'),
                    ('CI', 'Costa do Marfim'),
                    ('KE', 'Quênia'),
                    ('LS', 'Lesoto'),
                    ('LR', 'Libéria'),
                    ('LY', 'Líbia'),
                    ('MG', 'Madagascar'),
                    ('MW', 'Malawi'),
                    ('ML', 'Mali'),
                    ('MR', 'Mauritânia'),
                    ('MU', 'Maurício'),
                    ('MA', 'Marrocos'),
                    ('MZ', 'Moçambique'),
                    ('NA', 'Namíbia'),
                    ('NE', 'Níger'),
                    ('NG', 'Nigéria'),
                    ('RW', 'Ruanda'),
                    ('ST', 'São Tomé e Príncipe'),
                    ('SN', 'Senegal'),
                    ('SC', 'Seychelles'),
                    ('SL', 'Serra Leoa'),
                    ('SO', 'Somália'),
                    ('ZA', 'África do Sul'),
                    ('SS', 'Sudão do Sul'),
                    ('SD', 'Sudão'),
                    ('SZ', 'Suazilândia'),
                    ('TZ', 'Tanzânia'),
                    ('TG', 'Togo'),
                    ('TN', 'Tunísia'),
                    ('UG', 'Uganda'),
                    ('ZM', 'Zâmbia'),
                    ('ZW', 'Zimbábue'),
                    # ASIA
                    ('AF', 'Afeganistão'),
                    ('AM', 'Armênia'),
                    ('AZ', 'Azerbaijão'),
                    ('BH', 'Bahrein'),
                    ('BD', 'Bangladesh'),
                    ('BT', 'Butão'),
                    ('BN', 'Brunei'),
                    ('KH', 'Camboja'),
                    ('CN', 'China'),
                    ('CY', 'Chipre'),
                    ('GE', 'Geórgia'),
                    ('IN', 'Índia'),
                    ('ID', 'Indonésia'),
                    ('IR', 'Irã'),
                    ('IQ', 'Iraque'),
                    ('IL', 'Israel'),
                    ('JP', 'Japão'),
                    ('JO', 'Jordânia'),
                    ('KZ', 'Cazaquistão'),
                    ('KW', 'Kuwait'),
                    ('KG', 'Quirguistão'),
                    ('LA', 'Laos'),
                    ('LB', 'Líbano'),
                    ('MY', 'Malásia'),
                    ('MV', 'Maldivas'),
                    ('MN', 'Mongólia'),
                    ('MM', 'Myanmar'),
                    ('NP', 'Nepal'),
                    ('KP', 'Coreia do Norte'),
                    ('OM', 'Omã'),
                    ('PK', 'Paquistão'),
                    ('PS', 'Territórios Palestinos'),
                    ('PH', 'Filipinas'),
                    ('QA', 'Catar'),
                    ('SA', 'Arábia Saudita'),
                    ('SG', 'Singapura'),
                    ('KR', 'Coreia do Sul'),
                    ('LK', 'Sri Lanka'),
                    ('SY', 'Síria'),
                    ('TW', 'Taiwan'),
                    ('TJ', 'Tajiquistão'),
                    ('TH', 'Tailândia'),
                    ('TL', 'Timor-Leste'),
                    ('TR', 'Turquia'),
                    ('TM', 'Turcomenistão'),
                    ('AE', 'Emirados Árabes Unidos'),
                    ('UZ', 'Uzbequistão'),
                    ('VN', 'Vietnã'),
                    ('YE', 'Iêmen'),
                    # oceania
                    ('AS', 'Samoa Americana'),
                    ('AU', 'Austrália'),
                    ('CK', 'Ilhas Cook'),
                    ('FJ', 'Fiji'),
                    ('PF', 'Polinésia Francesa'),
                    ('GU', 'Guam'),
                    ('KI', 'Kiribati'),
                    ('MH', 'Ilhas Marshall'),
                    ('FM', 'Micronésia'),
                    ('NR', 'Nauru'),
                    ('NC', 'Nova Caledônia'),
                    ('NZ', 'Nova Zelândia'),
                    ('NU', 'Niue'),
                    ('NF', 'Ilha Norfolk'),
                    ('MP', 'Ilhas Marianas do Norte'),
                    ('PW', 'Palau'),
                    ('PG', 'Papua Nova Guiné'),
                    ('PN', 'Pitcairn'),
                    ('WS', 'Samoa'),
                    ('SB', 'Ilhas Salomão'),
                    ('TK', 'Tokelau'),
                    ('TO', 'Tonga'),
                    ('TV', 'Tuvalu'),
                    ('VU', 'Vanuatu'),
                    ('WF', 'Wallis e Futuna'),
                ),
        required=False,
            widget=forms.CheckboxSelectMultiple
        )

class TaxonStep7Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['distribuicao_biomas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['distribuicao_biomas'] = forms.MultipleChoiceField(
            choices=[
                ('CERRADO', 'Cerrado'),
                ('AMAZONIA', 'Amazônia'),
                ("CAATINGA", 'Caatinga'),
                ("PANTANAL", 'Pantanal'),
                ("PAMPA", 'Pampa'),
                ('MATAATLANTICA', 'Mata Atlântica'),
            ],
            required=False,
            widget=forms.CheckboxSelectMultiple
        )

class TaxonStep8Form(BaseTaxonForm):
    class Meta:
        model = Taxon
        fields = ['fitofisionomias']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fitofisionomias'] = forms.MultipleChoiceField(
            choices=[
                ('AREAANTROPICA', 'Área antrópica'),
                ('CAATINGA', 'Caatinga'),
                ('CAMPINARANA', 'Campinarana'),
                ('CAMPOLIMPOSECO', 'Campo limpo seco'),
                ('CAMPOLIMPOUMIDO', 'Campo limpo úmido'),
                ('TURFEIRA', 'Turfeira (peatland)'),
                ('CAMPODEALTITUDE', 'Campo de altitude'),
                ('CAMPODEVARZEA', 'Campo de várzea'),
                ('CAMPORUPESTREQUARTZITICO', 'Campo rupestre quartzítico'),
                ('CAMPORUPESTREFERRUGINOSO', 'Campo rupestre ferruginoso'),
                ('INSELBERG', 'Inselberg (granito/gnaisse)'),
                ('CARSTICAS', 'Feições cársticas'),
                ('CARRASCO', 'Carrasco'),
                ('CERRADAO', 'Cerradão'),
                ('CERRADOSTRICTOSENSU', 'Cerrado stricto sensu'),
                ('CAMPOSUJO', 'Campo Sujo'),
                ('FLORESTACILIAR', 'Floresta Ciliar e/ou de Galeria'),
                ('FLORESTADEIGAPO', 'Floresta de Igapó'),
                ('FLORESTADETERRAFIRME', 'Floresta de Terra-Firme'),
                ('FLORESTADEVARZEA', 'Floresta de Várzea'),
                ('FLORESTAESTACIONALDECIDUAL', 'Floresta Estacional Decidual'),
                ('FLORESTAESTACIONALPERENIFOLIA', 'Floresta Estacional Perenifólia'),
                ('FLORESTASEMIDECIDUAL', 'Floresta Semidecidual'),
                ('FLORESTAOMBROFILA', 'Floresta Ombrófila (Floresta Pluvial)'),
                ('FLORESTAOMBROFILAMISTA', 'Floresta Ombrófila Mista'),
                ('MANGUEZAL', 'Manguezal'),
                ('VEREDA', 'Vereda (buritizal)'),
                ('RESTINGA', 'Restinga'),
                ('SAVANA', 'Savana Amazônica'),
                ('VEGETACAOAQUATICA', 'Vegetação aquática'),
                ('EMAFLORAMENTOSROCHOSOSQUARTZITICOS', 'em afloramentos rochosos quartzíticos'),
                ('EMAFLORAMENTOSROCHOSOSGRANITICOS', 'em afloramentos rochosos graníticos'),
                ('EMAFLORAMENTOSFERRUGINOSOS', 'em afloramentos rochosos ferruginosos'),
            ],
            required=False,
            widget=forms.CheckboxSelectMultiple
        )

class TaxonStep9Form(BaseTaxonForm):
    class Meta:
        model = Taxon  # Define o modelo corretamente
        fields = ['distribuicoes_formacoes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['distribuicoes_formacoes'] = forms.MultipleChoiceField(
            choices=[
                ('ESPINHACO', 'Serra do Espinhaço'),
                ('MANTIQUEIRA', 'Serra da Mantiqueira'),
                ('CANASTRA', 'Serra da Canastra'),
                ('CAPIVARA', 'Serra da Capivara'),
                ('DIAMANTINA', 'Chapada Diamantina'),
                ('VEADEIROS', 'Chapada dos Veadeiros'),
                ('GUIMARAES', 'Chapada dos Guimarães'),
                ('IBITIPOCA', 'Serra de Ibitipoca'),
                ('CABRAL', 'Serra do Cabral'),
                ('AMBROSIO', 'Serra do Ambrósio'),
                ('ANGELO', 'Serra do Padre Ângelo'),
                ('MAR', 'Serra do Mar'),
                ('SERRA', 'Aparados da Serra'),
                ('CARAJAS', 'Serra dos Carajás'),
                ('TPEQUEM', 'Serra de Tapequém (RR)'),
                ('CARACA', 'Serra do Caraça'),
                ('BOCAINA', 'Complexo de Serras da Bocaina'),
                ('ITATIAIA', 'Serra de Itatiaia'),
                ('CIPO', 'Serra do Cipó'),
                ('INTENTENDE', 'Serra do Intendente'),
                ('NEGRA', 'Serra Negra (Itamarandiba, MG)'),
                ('NOVA', 'Serra Nova (MG)'),
                ('RORAIMA', 'Monte Roraima'),
                ('NEBLINA', 'Pico da Neblina'),
            ],
            required=False,
            widget=forms.CheckboxSelectMultiple
        )

    