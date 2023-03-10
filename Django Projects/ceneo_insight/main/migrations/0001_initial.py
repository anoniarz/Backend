# Generated by Django 4.1.5 on 2023-03-10 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=36)),
                ('product_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_id', models.IntegerField()),
                ('review_id', models.CharField(max_length=36)),
                ('author', models.CharField(max_length=255)),
                ('is_recomended', models.CharField(max_length=20)),
                ('is_verified', models.BooleanField()),
                ('stars', models.CharField(max_length=255)),
                ('date_p', models.DateTimeField()),
                ('date_b', models.DateTimeField()),
                ('t_up', models.IntegerField()),
                ('t_down', models.IntegerField()),
                ('opinion', models.TextField()),
                ('pos_features', models.JSONField()),
                ('neg_features', models.JSONField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_reviews', to='main.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ManyToManyField(related_name='reviews', to='main.review'),
        ),
    ]
