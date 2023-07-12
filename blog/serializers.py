from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['author', 'id', 'title', 'content', 'date_po