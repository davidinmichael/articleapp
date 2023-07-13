from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ['author', 'id', 'title', 'content', 'category', 'date_posted']
        extra_kwargs = {
            'author': {'read_only': True},
            'id': {'read_only': True}
        }

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
        extra_kwargs = {
            'name': {'read_only': True}
        }