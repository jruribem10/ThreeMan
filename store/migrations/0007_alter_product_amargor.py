# Generated by Django 5.0.1 on 2024-03-21 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amargor',
            field=models.CharField(choices=[('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')], max_length=255),
        ),
    ]