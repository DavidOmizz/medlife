# Generated by Django 4.2.7 on 2023-11-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
