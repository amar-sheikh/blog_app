from app.models import Article, Author, Tag
from datetime import timedelta, datetime
from django.views.generic import ListView
from django.utils import timezone

class AuthorListView(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'authors/author_list.html'
    paginate_by = 10

    def get_queryset(self):
        top_active_authors = bool(self.request.GET.get('top_active_authors', 0))
        date_time = self.request.GET.get('date_time')
        published = self.request.GET.get('published', 'all')
        with_articles = bool(self.request.GET.get('with_articles', 0))
        article_titles = self.request.GET.getlist('article_titles[]', None)
        tagged = bool(self.request.GET.get('tagged', 0))
        tag_names = self.request.GET.getlist('tag_names[]', None)

        if top_active_authors:
            if not date_time:
                date_time = timezone.now() - timedelta(days=365)
            else:
                date_time = datetime.fromisoformat(date_time)
            return Author.objects.top_active_authors(date_time=date_time, tag_names=tag_names)

        queryset= Author.objects.all()

        if published == 'True':
            queryset = queryset.with_published_articles()

        if published == 'False':
            queryset = queryset.with_un_published_articles()

        if with_articles:
            queryset = queryset.with_articles(article_titles)

        if tagged:
            queryset = queryset.with_tagged_articles(tag_names)

        if date_time:
            queryset = queryset.active_since(datetime.fromisoformat(date_time))

        return queryset.order_by('id').select_related('user').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['articles'] = Article.objects.all().select_related('author')
        context['selected_article_titles'] = self.request.GET.getlist('article_titles[]')
        context['selected_tag_names'] = self.request.GET.getlist('tag_names[]')
        return context
