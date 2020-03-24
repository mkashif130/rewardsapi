# Generated by Django 2.0.2 on 2020-03-16 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20200316_2315'),
        ('store', '0006_auto_20200316_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('profile_image', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_at', models.DateTimeField(null=True)),
                ('profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Profile')),
            ],
            options={
                'verbose_name_plural': 'Public',
            },
        ),
        migrations.AddField(
            model_name='store',
            name='store_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.StoreOwner'),
        ),
    ]