from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView
from bookmarker.models import Bookmark
from django.contrib.auth.mixins import LoginRequiredMixin

# views

class BookmarkerIndexView(TemplateView):
    template_name = "bookmarker/index.html"

class BookmarksListView(LoginRequiredMixin, ListView):
    template_name = 'bookmarker/list_view.html'
    model = Bookmark
    context_object_name = 'user_bookmarks'

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        return Bookmark.objects.filter(owner=user.pk)

