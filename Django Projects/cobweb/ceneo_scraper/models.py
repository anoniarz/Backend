from django.db import models


class Product(models.Model):
    product_id = models.CharField(
        max_length=36, primary_key=True)
    product_name = models.CharField(max_length=255)
    product_rating = models.CharField(max_length=10)
    product_category = models.CharField(max_length=50)
    product_price = models.FloatField()
    reviews = models.ManyToManyField('Review', related_name='reviews')

    def __str__(self):
        return self.product_name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='products_reviews')
    review_id = models.CharField(
        max_length=36)
    author = models.CharField(max_length=255)
    stars = models.CharField(max_length=255)
    recommendation = models.CharField(max_length=255)
    is_verified = models.BooleanField()
    date_p = models.DateTimeField()
    date_b = models.DateTimeField()
    days_used = models.IntegerField()
    t_up = models.IntegerField()
    t_down = models.IntegerField()
    opinion = models.TextField()
    pos_features = models.JSONField()
    neg_features = models.JSONField()

    def __str__(self):
        return f"{self.author} - {self.review_id}"
