# Generated by Django 2.2.4 on 2019-08-25 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0002_auto_20190818_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizens',
            name='building',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='citizens',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='citizens',
            name='street',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='citizens',
            name='town',
            field=models.CharField(max_length=256),
        ),
    ]
