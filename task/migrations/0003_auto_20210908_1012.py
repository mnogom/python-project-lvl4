# Generated by Django 3.2.7 on 2021-09-08 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
        ('task', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='label.label')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='task.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(through='task.TaskLabel', to='label.Label'),
        ),
    ]
