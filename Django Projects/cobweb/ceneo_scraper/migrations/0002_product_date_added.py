# Generated by Django 4.1.5 on 2023-03-31 23:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ceneo_scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
