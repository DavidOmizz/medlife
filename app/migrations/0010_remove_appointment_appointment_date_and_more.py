# Generated by Django 4.2.7 on 2024-01-19 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_comment_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_time',
        ),
    ]
