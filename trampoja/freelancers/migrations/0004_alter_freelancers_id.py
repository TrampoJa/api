# Generated by Django 3.2 on 2021-05-11 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0003_auto_20201110_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancers',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
