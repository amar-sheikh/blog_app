from django.db import models
from .author import Author
from .tag import Tag

class Article(models.Model):
    author=models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    tags=models.ManyToManyField(Tag, related_name='articles')

    title=models.CharField(max_length=255)
    content=models.TextField()
    is_published=models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
