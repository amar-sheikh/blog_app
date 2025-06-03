from django.db import models
from .article import Article
from .user import User

class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article=models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    content=models.TextField()
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
