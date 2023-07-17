from os import name
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.SET_NULL, null=True, blank=True)
    date_posted = models.DateField(default=date.today)
    is_public = models.BooleanField(default=True)
    slug = models.CharField(max_length=800, blank=True)
    article_likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + '-' + str(self.author))
        return super().save(*args, **kwargs)

class ArticleComment(models.Model):
    comment = models.TextField()
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='blog_comment')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.article)