from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView

from data.models import Summary, Region


class LatestSummaryMixin:
    def get_summary(self):
        return Summary.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = self.get_summary()
        return context


class IndexPageView(LatestSummaryMixin, TemplateView):
    template_name = "index.html"


class RegionsListView(LatestSummaryMixin, ListView):
    context_object_name = "regions"
    template_name = "regions.html"
    paginate_by = 30

    def get_queryset(self):
        summary = self.get_summary()
        if summary:
            return summary.regions_data
        return []


class RegionDetailView(LatestSummaryMixin, DetailView):
    context_object_name = "region"
    template_name = "region.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs.get("region").lower()
        summary = self.get_summary()
        try:
            region = Region(slug=slug, summary=summary)
            return region
        except ValueError:
            return
