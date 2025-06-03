from django.db import models
from django.db.models.aggregates import Count
from django.db.models import Q
from .user import User

class AuthorQuerySet(models.QuerySet):
    def active_since(self, date_time):
        return self.with_published_articles().filter(articles__published_at__gte=date_time).distinct()

    def with_articles(self, article_titles=None):
        queryset = self.filter(articles__isnull=False)
        if article_titles:
            queryset = queryset.filter(articles__title__in=article_titles)
        return queryset

    def with_published_articles(self):
        return self.filter(articles__is_published=True)

    def with_tagged_articles(self, tag_name=None):
        if tag_name:
            return self.filter(articles__tags__name=tag_name)
        return self.filter(articles__tags__isnull=False)

    def top_active_authors(self, tag_name, since_date):
        return (
            self.active_after(since_date)
                .with_tagged_articles(tag_name)
                .annotate(
                    approved_comment_count=Count(
                        "comment",
                        filter=Q(comment__is_approved=True),
                        distinct=True
                    )
                )
                .filter(approved_comment_count__gte=5)
        )

class Author(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.CharField(max_length=255, null=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    objects = AuthorQuerySet.as_manager()

    def __str__(self):
        return self.user.username
