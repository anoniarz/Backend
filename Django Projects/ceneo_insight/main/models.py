from django.db import models


class Product(models.Model):
    product_id = models.CharField(
        max_length=36)
    product_name = models.CharField(max_length=255)
    reviews = models.ManyToManyField('Review', related_name='reviews')

    def __str__(self):
        return self.product_name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='products_reviews')
    local_id = models.IntegerField()
    review_id = models.CharField(
        max_length=36)
    author = models.CharField(max_length=255)
    is_recomended = models.CharField(max_length=255)
    is_verified = models.BooleanField()
    stars = models.CharField(max_length=255)
    date_p = models.DateTimeField()
    date_b = models.DateTimeField()
    t_up = models.IntegerField()
    t_down = models.IntegerField()
    opinion = models.TextField()
    pos_features = models.JSONField()
    neg_features = models.JSONField()

    def __str__(self):
        return f"{self.author} - {self.review_id}"
