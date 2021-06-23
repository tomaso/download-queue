# Generated by Django 3.2 on 2021-04-22 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dq", "0002_alter_downloadjob_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="downloadjob",
            name="queue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dq.queue",
            ),
        ),
    ]