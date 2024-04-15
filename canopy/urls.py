from django.urls import path

from .views import ControllerFormView, ControllerSuccessView

app_name = "canopy"


urlpatterns = [
    path("form/success/", ControllerSuccessView.as_view(), name="controller-success"),

    path(
        "form/<slug:slug>/",
        ControllerFormView.as_view(),
        name="controller-form"
    ),
]
