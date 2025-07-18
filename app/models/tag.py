from django.db import models

class Tag(models.Model):
    name=models.CharField(max_length=64)
    description=models.CharField(max_length=255)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name