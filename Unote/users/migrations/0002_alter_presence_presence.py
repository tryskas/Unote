# Generated by Django 4.1 on 2024-06-05 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="presence",
            name="presence",
            field=models.CharField(max_length=30),
        ),
    ]
