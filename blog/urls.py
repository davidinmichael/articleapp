from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListCreate.as_view(), name="article-home"),
    path("blog-detail/<str:pk>/", views.ArticleUpdate.as_view(), name="article-detail"),
    path("categories/", views.CategoryList.as_view(), name="category-list"),
    path("users/", views.UserList.as_view(), name="users"),
    path("users/<str:username>/", views.UserDetail.as_view(), name="user-detail"),
    path("blog-comment/<str:article_id>/", views.ArticleCommentView.as_view(), name="article-comment"),
    path("article-like/<int:pk>/", views.ArticleLikes.as_view(), name='like'),
    # path("article-dislike/<int:pk>/", views.ArticleDislikes.as_view(), name='dislike'),
]
