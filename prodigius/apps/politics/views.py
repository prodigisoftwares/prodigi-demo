import math

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .models import Politician, Question, TestSubmission
from .utils import compute_coords


class IndexView(TemplateView):
    template_name = "politics/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["questions"] = Question.objects.all()
        return ctx


class TakeView(TemplateView):
    template_name = "politics/take.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["questions"] = Question.objects.prefetch_related("choices").all()
        return ctx


class ScoreView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        answers = {
            f"q{i}": request.POST.get(f"q{i}", "")
            for i in range(1, 13)
            if request.POST.get(f"q{i}")
        }
        x, y = compute_coords(answers)
        sub = TestSubmission.objects.create(answers=answers, x=x, y=y)

        def dist(p):
            return math.hypot(p.x - x, p.y - y)

        nearest = sorted(list(Politician.objects.all()), key=dist)[:3]
        ctx = {"submission": sub, "nearest": nearest, "x": x, "y": y}
        return render(request, "politics/partials/result.html", ctx)

    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponseBadRequest("Use POST")
