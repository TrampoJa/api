# Generated by Django 3.2 on 2021-05-11 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cancelados', '0002_cancelados_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelados',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
