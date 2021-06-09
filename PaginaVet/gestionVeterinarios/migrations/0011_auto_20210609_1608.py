# Generated by Django 3.2 on 2021-06-09 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVeterinarios', '0010_auto_20210429_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='user',
            name='region',
        ),
        migrations.AddField(
            model_name='user',
            name='veterinario',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='gestionVeterinarios.veterinario'),
        ),
    ]