# Generated by Django 2.2.4 on 2019-08-16 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relatives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizen_1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citizen_1_id', to='citizens.Citizens')),
                ('citizen_2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citizen_2_id', to='citizens.Citizens')),
                ('import_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citizens.Imports')),
            ],
        ),
    ]
