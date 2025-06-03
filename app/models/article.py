from django.db import models
from .auther import Auther
from .tag import Tag

class Article(models.Model):
    author=models.ForeignKey(Auther, on_delete=models.CASCADE, related_name='articles')
    tags=models.ManyToManyField(Tag, related_name='articles')

    title=models.CharField(max_length=255)
    content=models.TextField()
    is_published=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
