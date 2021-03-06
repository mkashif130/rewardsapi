# Generated by Django 2.0.2 on 2020-03-24 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20200324_1723'),
        ('public', '0004_public_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('public', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='public.Public')),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
            ],
        ),
    ]
