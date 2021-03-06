# Generated by Django 3.2.5 on 2021-08-24 01:32

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('freelancers', '0008_freelancers_verificado'),
        ('ofertas', '0006_auto_20210511_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.IntegerField()),
                ('nome', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Reportes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancers.freelancers')),
                ('motivos', models.ManyToManyField(to='reportes.Motivos')),
                ('trampo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofertas.ofertas')),
            ],
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
