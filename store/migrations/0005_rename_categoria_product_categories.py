# Generated by Django 5.0.1 on 2024-03-13 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_estilos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='categoria',
            new_name='categories',
        ),
    ]