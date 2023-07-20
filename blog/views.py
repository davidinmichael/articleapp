from tokenize import Comment
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions, authentication
from .permissions import *

class ArticleListCreate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        articles = Article.objects.filter(is_public=True).order_by('-id')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save(author=request.user)
            article_serializer = ArticleSerializer(article)
            return Response(article_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
class ArticleUpdate(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, pk):
        article = Article.objects.get(is_public=True, id=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        article = Article.objects.get(is_public=True, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        article = Article.objects.get(is_public=True, pk=pk)
        article.delete()
        return Response({'message': 'Blog Successfully Deleted'}, status=status.HTTP_200_OK)

class CategoryList(APIView):
    permission_classes = [CategoryPermission]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
class UserDetail(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        articles = Article.objects.filter(author=user)
        serializedArticles = ArticleSerializer(articles, many=True)
        return Response({
            'user': serializer.data,
            'articles': serializedArticles.data
        })

class ArticleCommentView(APIView):
    def get(self, request, article_id):
        article_comments = ArticleComment.objects.filter(article_id=article_id)
        serializer = CommentSerializer(article_comments, many=True)
        return Response({"comments": serializer.data})
    
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comment = ArticleComment(article=article, comment_author=request.user, comment=request.data['comment'])
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

class ArticleLikes(APIView):
    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        user = request.user

        if article.article_likes.filter(id=user.id).exists():
            article.article_likes.remove(user)
            message = 'Article Disliked Successfully'
            liked = False
        else:
            article.article_likes.add(user)
            message = 'Article Liked Successfully'
            liked = True

        article.save()

        response_data = {
            'message': message,
            'total_likes': article.article_likes.count(),
            'liked': liked,
        }

        return Response(response_data)

class UserLikedArticles(APIView):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        liked_articles = Article.objects.filter(article_likes=user).order_by('-id')
        user_serializer = UserSerializer(user)
        articles_serialized = ArticleSerializer(liked_articles, many=True)
        response_data = {
            "user": user_serializer.data,
            "articles": articles_serialized.data,
        }
        return Response(response_data)