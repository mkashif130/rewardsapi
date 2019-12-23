# Generated by Django 2.0.2 on 2019-12-23 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicRedeems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='public',
            name='total_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='publicredeems',
            name='public',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Public'),
        ),
        migrations.AddField(
            model_name='publicredeems',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store'),
        ),
    ]
