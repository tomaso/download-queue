# Generated by Django 3.2 on 2021-04-21 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Queue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("paused", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="DownloadJob",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("target_directory", models.CharField(max_length=256)),
                ("url", models.CharField(max_length=1024)),
                ("completed", models.BooleanField(default=False)),
                ("priority", models.DecimalField(decimal_places=10, max_digits=10)),
                (
                    "queue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dq.queue"
                    ),
                ),
            ],
        ),
    ]
