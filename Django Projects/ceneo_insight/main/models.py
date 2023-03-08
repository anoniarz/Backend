from django.db import models

class Reviews(models.Model):
    local_id = models.IntegerField()
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    review_id = models.CharField(max_length=50, unique=True)
    author = models.CharField(max_length=50)
    is_recomended = models.BooleanField()
    is_verified = models.BooleanField()
    stars = models.CharField(max_length=5)
    date_p = models.DateTimeField()
    date_b = models.DateTimeField()
    t_up = models.IntegerField()
    t_down = models.IntegerField()
    opinion = models.TextField()
    pos_features = models.JSONField(default=list)
    neg_features = models.JSONField(default=list)

    def __str__(self):
        return self.review_id