from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Article(models.Model):
    link = models.URLField(null=True)
    title = models.TextField(null=True)
    body = models.TextField(null=True)
    fake = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="article_list")
    posted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
