from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    # category = serializers.StringRelatedField()
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='name', allow_null=True)

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

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['category'] = instance.category.name
    #     return representation

class CategorySerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ['name', 'articles']
        extra_kwargs = {
            'name': {'read_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']