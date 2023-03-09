# Generated by Django 4.0.5 on 2023-03-09 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_review_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='product_name',
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=255)),
                ('reviews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.reviews')),
            ],
        ),
    ]
