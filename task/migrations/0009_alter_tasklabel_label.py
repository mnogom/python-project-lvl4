# Generated by Django 3.2.7 on 2021-09-08 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
        ('task', '0008_auto_20210908_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklabel',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='label.label'),
        ),
    ]
