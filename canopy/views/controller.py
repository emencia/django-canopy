from django import forms
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from ..models import Controller
from ..forms.forge import FormClassForge


class ControllerFormView(FormView):
    """
    View to display a Controller form.

    TODO: Help i'm not tested yet.
    """
    template_name = "canopy/controller/form.html"
    form_class = forms.Form  # Not used
    success_url = reverse_lazy("canopy:controller-success")

    def get_object(self):
        try:
            obj = Controller.objects.get(slug=self.kwargs["slug"])
        except Controller.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": Controller._meta.verbose_name}
            )

        return obj

    def get_context_data(self, **kwargs):
        kwargs["controller"] = self.object

        if "form" not in kwargs:
            kwargs["form"] = self.get_form()

        return super().get_context_data(**kwargs)

    def get_form_class(self):
        """
        Build controller form using forge.
        """
        forge = FormClassForge()
        return forge.get_form(self.object)

    def get_form_kwargs(self):
        """
        Give controller object as form argument.
        """
        kwargs = super().get_form_kwargs()
        kwargs["controller"] = self.object
        return kwargs

    def form_valid(self, form):
        """
        Save request as an Entry when submitted form data has been validated.
        """
        created = form.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Display blank form
        """
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Receive request and save or display errors.
        """
        self.object = self.get_object()
        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form)


class ControllerSuccessView(TemplateView):
    """
    Basic template view to respond to form submit success.

    TODO: Success view need to have the controller object it come from so the view
    could use some Controller options (like custom template, custom success message,
    etc..)
    """
    template_name = "canopy/controller/success.html"
