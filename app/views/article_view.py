from django.views.generic import ListView
from app.models import Article, Author, Tag

class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/article_list.html'
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        days = int(self.request.GET.get('days', 0) or 0)
        published = self.request.GET.get('published', 'all')
        author_names = self.request.GET.getlist('author_names[]', None)
        special = self.request.GET.get('special', '')
        tagged = bool(self.request.GET.get('tagged', 0))
        tag_names = self.request.GET.getlist('tag_names[]', None)
        with_approved_comment = bool(self.request.GET.get('with_approved_comment', 0))
        comments_count = int(self.request.GET.get('comments_count', 0) or 0)

        queryset = Article.objects.all()

        if search:
            queryset = queryset.search(search)

        if author_names:
            queryset = queryset.by_author(author_names)

        if special == 'hot':
            comments_count = max(comments_count, 1)
            days = max(days, 7)
            queryset = Article.objects.hot_articles(days=days, tag_names=tag_names)
        elif special == 'trending':
            comments_count = max(comments_count, 5)
            days = max(days, 3)
            return Article.objects.trending(
                days=days,
                min_comments=comments_count,
                tag_names=tag_names
            ).select_related('author__user')
        else:
            if tagged:
                queryset = queryset.tagged(tag_names)

            if with_approved_comment:
                if comments_count > 0:
                    queryset = queryset.with_approved_comments(comments_count)
                else:
                    queryset = queryset.with_approved_comments(1)

            if published == 'True':
                queryset = queryset.published()
            elif published == 'False':
                queryset = queryset.un_published()

            if days > 0:
                queryset = queryset.recent(days)

        return queryset.order_by('id').select_related('author__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['authors'] = Author.objects.all().select_related('user')
        context['selected_author_names'] = self.request.GET.getlist('author_names[]')
        context['selected_tag_names'] = self.request.GET.getlist('tag_names[]')
        return context
