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

    def with_tagged_articles(self, tag_names=None):
        if tag_names:
            return self.filter(articles__tags__name__in=tag_names).distinct()
        return self.filter(articles__tags__isnull=False).distinct()

    def top_active_authors(self, date_time, tag_names=None, min_comments=5):
        if min_comments < 5:
            raise ValueError("count can't be less than 5")

        return (
            self.active_since(date_time)
                .with_tagged_articles(tag_names)
                .annotate(
                    approved_comment_count=Count(
                        "articles__comments",
                        filter=Q(articles__comments__is_approved=True),
                        distinct=True
                    )
                )
                .filter(approved_comment_count__gte=min_comments)
                .order_by('-approved_comment_count')
        )

class Author(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.CharField(max_length=255, null=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    objects = AuthorQuerySet.as_manager()

    def __str__(self):
        return self.user.username
