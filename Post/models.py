from django.db import models
from Article.models import Article

# Create your models here.


class Post(models.Model):
    posted_on = models.DateField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
