import os
import django
# Comando para rodar este script e cadastrar as espécies: docker-compose exec web python import_taxons.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semprevivas.settings')
django.setup()

import json
from datetime import datetime
from django.utils.timezone import make_aware
from eriocaulaceae.models import Taxon

def parse_data(data_string):
    try:
        return make_aware(datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S.%f"))
    except ValueError:
        return make_aware(datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S"))

def run():
    with open("data/response_1750506422595.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    for item in dados:
        taxon = Taxon(
            taxonID=item.get("taxonid"),
            scientificName=item.get("scientificname"),
            taxonRank=item.get("taxonrank"),
            nomenclaturalStatus=item.get("nomenclaturalstatus"),
            taxonomicStatus=item.get("taxonomicstatus"),
            kingdom=item.get("kingdom"),
            phylum=item.get("phylum"),
            classe=item.get("class"),
            order=item.get("order"),
            family=item.get("family"),
            genus=item.get("genus"),
            specificEpithet=item.get("specificepithet"),
            infraspecificEpithet=item.get("infraspecificepithet"),
            scientificNameAuthorship=item.get("scientificnameauthorship"),
            acceptedNameUsage=item.get("acceptednameusage"),
            higherClassification=item.get("higherclassification"),
            parentNameUsage=item.get("parentnameusage"),
            parentNameUsageID=item.get("parentnameusageid"),
            originalNameUsageID=int(item["originalnameusageid"]) if item.get("originalnameusageid") else None,
            namePublishedIn=item.get("namepublishedin"),
            namePublishedInYear=item.get("namepublishedinyear"),
            references=item.get("references"),
            bibliographicCitation=item.get("bibliographiccitation_how_to_cite"),
            modified=parse_data(item["modified"]) if item.get("modified") else None,
            status=True,
        )
        taxon.save()
        print(f"Taxon salvo: {taxon.scientificName}")

if __name__ == "__main__":
    run()
