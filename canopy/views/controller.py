from django import forms
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


class ControllerFormView(FormView):
    """
    View to display a Controller form.

    TODO: Currently not working until form builder is done.
    """
    template_name = "canopy/controller/form.html"
    form_class = forms.Form
    success_url = reverse_lazy("canopy:request-success")

    def get_form_class(self):
        """
        TODO: Here we would use FormClassBuilder to build form fields dynamically from
        controller slots.
        """
        return self.form_class

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form)


class ControllerSuccessView(TemplateView):
    """
    Basic template view to respond to form submit success.
    """
    template_name = "canopy/controller/success.html"
