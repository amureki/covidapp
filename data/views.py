from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView

from data.models import Summary


@method_decorator(cache_page(settings.INDEX_PAGE_CACHE_TTL_SECONDS), name="dispatch")
class IndexPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = Summary.objects.first()
        return context


class CountriesListView(ListView):
    context_object_name = "countries"
    template_name = "countries.html"
    paginate_by = 30

    def get_queryset(self):
        if Summary.objects.exists():
            return Summary.objects.first().countries_data
        return []
