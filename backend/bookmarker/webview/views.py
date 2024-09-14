from django.views.generic import TemplateView

# views

class BookmarkerIndexView(TemplateView):
    template_name = "bookmarker/index.html"
