from django.urls import path
from ninja import NinjaAPI

from demo.api.views import router

api = NinjaAPI(title="prom-demo API", version="1.0.0")
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]
