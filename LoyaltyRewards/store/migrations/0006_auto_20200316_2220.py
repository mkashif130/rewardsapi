# Generated by Django 2.0.2 on 2020-03-16 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_store_qrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='qrcode',
            field=models.TextField(default=''),
        ),
    ]