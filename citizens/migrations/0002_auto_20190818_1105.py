# Generated by Django 2.2.4 on 2019-08-18 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizens',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=10),
        ),
    ]