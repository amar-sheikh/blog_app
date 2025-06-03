from django.db import models
from .user import User

class Author(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.CharField(max_length=255, null=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
