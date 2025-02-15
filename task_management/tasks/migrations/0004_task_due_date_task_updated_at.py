# Generated by Django 5.1.3 on 2024-11-27 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_task_updated_at_alter_task_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
