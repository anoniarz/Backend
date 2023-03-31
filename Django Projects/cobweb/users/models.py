from django.db import models
from django.contrib.auth.models import User
from ceneo_scraper.models import Product
from PIL import Image


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ceneo_favourites = models.ManyToManyField(
        Product, related_name='favourites')
    image = models.ImageField(
        default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def add_to_favourites(self, product):
        self.ceneo_favourites.add(product)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
