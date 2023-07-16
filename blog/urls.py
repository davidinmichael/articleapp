from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListCreate.as_view(), name="article-home"),
    path("<str:pk>/", views.ArticleUpdate.as_view(), name="article-detail"),
    path("category/all/", views.CategoryList.as_view(), name="category-list"),
    path("users/all/", views.UserList.as_view(), name="users"),
    path("users/<str:username>/", views.UserDetail.as_view(), name="user-detail"),
    path("blog-comment/<str:blog_id>/", views.ArticleCommentView.as_view(), name="article-comment"),
]
