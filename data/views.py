from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from data.models import Summary


@method_decorator(cache_page(settings.INDEX_PAGE_CACHE_TTL_SECONDS), name="dispatch")
class IndexPageView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = Summary.objects.first()
        return context
