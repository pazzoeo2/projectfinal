# Generated by Django 3.0.8 on 2020-09-24 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='finished',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='review',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='entry',
            name='started',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='entry',
            name='timeplayed',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]