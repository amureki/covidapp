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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline_data = self.get_timeline_data()
        dates_series = [
            dt.strftime("%d %b")
            for dt in timeline_data.values_list("created", flat=True)
        ]
        context["timeline"] = {
            "dates_series": dates_series,
            "confirmed_series": list(timeline_data.values_list("confirmed", flat=True)),
            "deaths_series": list(timeline_data.values_list("deaths", flat=True)),
            "recovered_series": list(timeline_data.values_list("recovered", flat=True)),
        }
        return context

    def get_timeline_data(self):
        summaries = Summary.objects.filter(is_latest_for_day=True).order_by("created")
        return summaries.values("confirmed", "deaths", "recovered", "created")


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
        self.slug = self.kwargs.get("region").lower()
        summary = self.get_summary()
        return self.get_region_or_none(summary)

    def get_region_or_none(self, summary):
        try:
            return Region(slug=self.slug, summary=summary)
        except ValueError:
            return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline_data = self.get_timeline_data()

        data_series = [
            (self.get_region_or_none(summary), summary.created)
            for summary in timeline_data
        ]

        data_series = [ds for ds in data_series if ds[0] is not None]

        dates_series = [ds[0].created.strftime("%d %b") for ds in data_series]
        confirmed_series = [ds[0].confirmed for ds in data_series]
        deaths_series = [ds[0].deaths for ds in data_series]
        recovered_series = [ds[0].recovered for ds in data_series]

        context["timeline"] = {
            "dates_series": dates_series,
            "confirmed_series": confirmed_series,
            "deaths_series": deaths_series,
            "recovered_series": recovered_series,
        }
        return context

    def get_timeline_data(self):
        summaries = Summary.objects.filter(is_latest_for_day=True).order_by("created")
        return summaries
