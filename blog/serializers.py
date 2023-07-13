from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['author', 'id', 'title', 'content', 'date_posted']
        extra_kwargs = {
            'author': {'read_only': True},
            'id': {'read_only': True}
        }

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance