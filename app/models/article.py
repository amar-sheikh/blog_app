from datetime import timedelta
from django.db import models
from django.db.models.aggregates import Count
from django.db.models import Q
from django.utils import timezone
from .author import Author
from .tag import Tag

class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def recent(self, days=7):
        return self.published().filter(published_at__gte=timezone.now() - timedelta(days))

    def tagged(self, tag_names=None):
        if tag_names:
            return self.filter(tags__name__in=tag_names).distinct()
        return self.filter(tags__isnull=False).distinct()

    def with_approved_comments(self, count=1):
        if count < 1:
            raise ValueError("count can't be less than 1")

        return (
            self.published()
                .annotate(
                    approved_comments_count=Count(
                        'comments',
                        filter=Q(comments__is_approved=True),
                        distinct=True
                    )
                ).filter(approved_comments_count__gte=count)
        )

    def search(self, text):
        return self.filter(Q(title__icontains=text) | Q(content__icontains=text))

    def by_author(self, author_names):
        return self.filter(author__user__username__in=author_names)

    def hot_articles(self, days=7, tag_names=None):
        return (
            self.recent(days)
                .tagged(tag_names)
                .with_approved_comments()
                .distinct()
        )

    def trending(self, min_comments=5, days=3, tag_names=None):
        if min_comments < 5:
            raise ValueError("count can't be less than 5")

        return (
            self
                .hot_articles(days, tag_names)
                .with_approved_comments(min_comments)
                .order_by('-approved_comments_count', '-published_at')[:5]
        )

class Article(models.Model):
    author=models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    tags=models.ManyToManyField(Tag, related_name='articles')

    title=models.CharField(max_length=255)
    content=models.TextField()
    is_published=models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return self.title
