from django.db import models
from .article import Article
from .user import User

class CommentQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(is_approved=True)

    def non_approved(self):
        return self.filter(is_approved=False)

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
