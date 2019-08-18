# Generated by Django 2.2.4 on 2019-08-17 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Citizens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizen_id', models.PositiveIntegerField()),
                ('town', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('building', models.CharField(max_length=255)),
                ('apartment', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('birth_date', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Imports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Relatives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizen_1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citizen_1_id', to='citizens.Citizens')),
                ('citizen_2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citizen_2_id', to='citizens.Citizens')),
                ('import_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citizens.Imports')),
            ],
        ),
        migrations.AddField(
            model_name='citizens',
            name='import_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='import_id', to='citizens.Imports'),
        ),
    ]
