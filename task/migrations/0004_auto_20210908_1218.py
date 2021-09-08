# Generated by Django 3.2.7 on 2021-09-08 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('status', '0002_status_created_at'),
        ('task', '0003_auto_20210908_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='status.status'),
        ),
        migrations.AlterField(
            model_name='tasklabel',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='label.label'),
        ),
        migrations.AlterField(
            model_name='tasklabel',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='task.task'),
        ),
    ]
