# Generated by Django 3.0.8 on 2020-09-24 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cover', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateField()),
                ('finished', models.DateField()),
                ('timeplayed', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('review', models.CharField(max_length=1000)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]