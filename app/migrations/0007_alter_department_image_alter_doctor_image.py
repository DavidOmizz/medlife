# Generated by Django 4.2.7 on 2023-11-28 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='image',
            field=models.ImageField(upload_to='department-images'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='image',
            field=models.ImageField(upload_to='doctor-images'),
        ),
    ]