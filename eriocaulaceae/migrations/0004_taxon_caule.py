# Generated by Django 5.0.3 on 2024-04-02 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eriocaulaceae", "0003_alter_taxon_acceptednameusageid"),
    ]

    operations = [
        migrations.AddField(
            model_name="taxon",
            name="caule",
            field=models.CharField(
                blank=True,
                choices=[
                    ("curto", "Curto"),
                    ("alongado", "Alongado"),
                    ("aereo", "Aéreo"),
                    ("ND", "Não determinado"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
