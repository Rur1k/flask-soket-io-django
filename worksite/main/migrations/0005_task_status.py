# Generated by Django 4.0.3 on 2022-04-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_task_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('new', 'Новая'), ('in_work', 'В работе'), ('completed', 'Выполнена'), ('cancel', 'Отмена'), ('refusal', 'Отказ')], default='new', max_length=16),
        ),
    ]
