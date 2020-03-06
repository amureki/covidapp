from django.views.generic import TemplateView

from data.parser import parse_data


class IndexPageView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        stats = parse_data()

        context = super().get_context_data(**kwargs)
        context["confirmed"] = stats["Confirmed"]
        context["deaths"] = stats["Deaths"]
        context["recovered"] = stats["Recovered"]
        return context
