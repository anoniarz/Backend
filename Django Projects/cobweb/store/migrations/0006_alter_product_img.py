# Generated by Django 4.0.5 on 2023-05-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(default='store_pics/default.jpg', upload_to='store_pics'),
        ),
    ]
