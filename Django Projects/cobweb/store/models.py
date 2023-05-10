from django.db import models
from django.utils import timezone
from PIL import Image

# Create your models here.

class Product(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    manufacturer = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    sold = models.IntegerField(default=0)

    img = models.ImageField(
        default='store_pics/default.jpg', upload_to='store_pics')
    model = models.CharField(max_length=50, blank=True)
    caliber = models.CharField(max_length=20, blank=True)
    weight = models.FloatField(blank=True)
    capacity = models.CharField(max_length=10, blank=True)


    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        img = Image.open(self.img.path)

        if img.height > 300 or img.width > 500:
            output_size = (300, 500)
            img.thumbnail(output_size)
            img.save(self.img.path)

    def __str__(self):
        return self.name
