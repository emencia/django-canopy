from django.urls import path

from .views import ControllerFormView, ControllerSuccessView

app_name = "canopy"


urlpatterns = [
    path("controller/", ControllerFormView.as_view(), name="controller-form"),
    path("success/", ControllerSuccessView.as_view(), name="controller-success"),
]
