# Generated by Django 3.1.2 on 2020-11-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertas', '0002_auto_20201029_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertas',
            name='edit',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
