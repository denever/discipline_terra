from django.views.generic import TemplateView

# Create your views here.

class CoverView(TemplateView):
    template_name = 'cover/cover.html'
