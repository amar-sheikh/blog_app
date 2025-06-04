from app.models import Comment, User
from datetime import timedelta
from django.views.generic import ListView
from django.utils import timezone

class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'comments/comment_list.html'
    paginate_by = 20

    def get_queryset(self):
        approved = self.request.GET.get('approved', 'all')
        user_id = self.request.GET.get('user_id', '')

        queryset= Comment.objects.all()

        if approved == 'True':
            queryset = queryset.approved()

        if approved == 'False':
            queryset = queryset.un_approved()
        
        if user_id:
            queryset = queryset.by_user(user_id)

        return queryset.select_related('user', 'article')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['selected_user_id'] = self.request.GET.get('user_id', '')
        return context
