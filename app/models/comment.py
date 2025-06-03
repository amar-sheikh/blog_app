from django.db import models
from .article import Article
from .user import User

class CommentQuerySet(models.QuerySet):
    def approved(self, user_id):
        queryset = self.filter(is_approved=True)
        if user_id:
            queryset = queryset.by_user(user_id)
        return queryset

    def non_approved(self, user_id):
        queryset = self.filter(is_approved=False)
        if user_id:
            queryset = queryset.by_user(user_id)
        return queryset

    def by_user(self, user_id):
        return self.filter(user__id=user_id)

class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article=models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    content=models.TextField()
    is_approved=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return self.title
