# Generated by Django 3.2 on 2021-04-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloadjob',
            name='priority',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
