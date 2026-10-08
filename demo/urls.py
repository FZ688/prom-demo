from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path("", include("django_prometheus.urls")),
    path("api/", include("demo.api.urls")),
    path("healthz", lambda r: HttpResponse("ok"), name="healthz"),
]
