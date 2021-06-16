# Generated by Django 3.2.4 on 2021-06-16 15:02

from django.db import migrations, models
import freelancers.models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0005_auto_20210615_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentos',
            name='frente',
            field=models.ImageField(blank=True, null=True, upload_to=freelancers.models.upload_path),
        ),
        migrations.AlterField(
            model_name='documentos',
            name='selfie',
            field=models.ImageField(blank=True, null=True, upload_to=freelancers.models.upload_path),
        ),
        migrations.AlterField(
            model_name='documentos',
            name='verso',
            field=models.ImageField(blank=True, null=True, upload_to=freelancers.models.upload_path),
        ),
    ]
