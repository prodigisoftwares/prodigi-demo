from django.urls import path

from .views import IndexView, ScoreView, TakeView

app_name = "politics"


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("test/", TakeView.as_view(), name="test"),
    path("score/", ScoreView.as_view(), name="score"),
]
