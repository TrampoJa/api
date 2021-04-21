# Generated by Django 3.1.2 on 2021-02-03 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ofertas', '0003_ofertas_edit'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancelados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('justificativa', models.TextField()),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('oferta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ofertas.ofertas')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'cancelado',
                'verbose_name_plural': 'cancelados',
                'ordering': ['oferta'],
            },
        ),
    ]
