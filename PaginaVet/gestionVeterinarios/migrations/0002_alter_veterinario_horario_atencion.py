# Generated by Django 3.2 on 2021-04-25 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVeterinarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinario',
            name='horario_atencion',
            field=models.CharField(max_length=300),
        ),
    ]