# Generated by Django 3.2 on 2021-05-11 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interesses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesses',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
