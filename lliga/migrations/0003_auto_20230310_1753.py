# Generated by Django 3.2 on 2023-03-10 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lliga', '0002_auto_20230310_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='partit',
            name='inici',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='jugador2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events2', to='lliga.jugador'),
        ),
        migrations.AlterField(
            model_name='event',
            name='temps',
            field=models.TimeField(),
        ),
    ]
