# Generated by Django 3.2 on 2021-05-26 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estabelecimentos', '0005_alter_estabelecimentos_managers'),
        ('planos', '0002_alter_planos_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estabelecimentos.estabelecimentos')),
                ('plano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planos.planos')),
            ],
            options={
                'verbose_name': 'historico',
                'verbose_name_plural': 'historicos',
                'ordering': ['create'],
            },
        ),
    ]
