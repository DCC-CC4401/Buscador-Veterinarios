# Generated by Django 3.2 on 2021-04-28 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVeterinarios', '0005_auto_20210427_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinario',
            name='foto',
            field=models.ImageField(blank=True, upload_to='fotos'),
        ),
    ]
