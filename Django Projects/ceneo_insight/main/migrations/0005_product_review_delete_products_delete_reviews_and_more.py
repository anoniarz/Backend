# Generated by Django 4.1.5 on 2023-03-09 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_products_product_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=255)),
                ('product_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_id', models.IntegerField()),
                ('review_Id', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('is_recomended', models.BooleanField()),
                ('is_verified', models.BooleanField()),
                ('stars', models.CharField(max_length=255)),
                ('date_p', models.DateTimeField()),
                ('date_b', models.DateTimeField()),
                ('t_up', models.IntegerField()),
                ('t_down', models.IntegerField()),
                ('opinion', models.TextField()),
                ('pos_features', models.JSONField()),
                ('neg_features', models.JSONField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.product')),
            ],
        ),
        migrations.DeleteModel(
            name='Products',
        ),
        migrations.DeleteModel(
            name='Reviews',
        ),
        migrations.AddField(
            model_name='product',
            name='reviewss',
            field=models.ManyToManyField(related_name='products', to='main.review'),
        ),
    ]
