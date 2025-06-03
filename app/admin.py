from django.contrib import admin
from .models import Article, Auther, Comment, Tag, User

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(Auther)
class AutherAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
