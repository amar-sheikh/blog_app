from django.urls import path
from app.views import ArticleListView, AuthorListView, CommentListView

urlpatterns = [
    path(r'articles', ArticleListView.as_view(), name='articles'),
    path(r'authors', AuthorListView.as_view(), name='authors'),
    path(r'comments', CommentListView.as_view(), name='comments')
]