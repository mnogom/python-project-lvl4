# Generated by Django 3.2.7 on 2021-09-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
    ]
