from django.views.generic import TemplateView, ListView

from data.models import Summary


class LatestSummaryMixin:
    def get_summary(self):
        return Summary.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = self.get_summary()
        return context


class IndexPageView(LatestSummaryMixin, TemplateView):
    template_name = "index.html"


class CountriesListView(LatestSummaryMixin, ListView):
    context_object_name = "countries"
    template_name = "countries.html"
    paginate_by = 30

    def get_queryset(self):
        summary = self.get_summary()
        if summary:
            return summary.regions_data
        return []
