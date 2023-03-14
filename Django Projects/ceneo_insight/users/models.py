from django.db import models
from django.contrib.auth.models import User
from main.models import Product


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourites = models.ManyToManyField(Product, related_name='favourites')

    def __str__(self):
        return f'{self.user.username} Profile'

    def add_to_favourites(self, product):
        self.favourites.add(product)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
