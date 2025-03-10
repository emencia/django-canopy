from django import forms
from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from ..models import Controller, Entry
from ..forms.forge import FormClassForge


class ControllerFormView(FormView):
    """
    View to display a Controller form.
    """
    template_name = "canopy/controller/form.html"
    form_class = forms.Form  # Not used

    def get_object(self):
        try:
            obj = Controller.objects.get(slug=self.kwargs["slug"])
        except Controller.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": Controller._meta.verbose_name}
            )

        return obj

    def get_success_url(self):
        return self.object.get_success_url()

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

    def form_valid(self, form):
        """
        Save request as an Entry when submitted form data has been validated.
        """
        created = form.save()
        self.request.session["canopy_last_entry_id"] = created.id

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
    """
    template_name = "canopy/controller/success.html"

    def get_controller_object(self):
        try:
            obj = Controller.objects.get(slug=self.kwargs["slug"])
        except Controller.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": Controller._meta.verbose_name}
            )

        return obj

    def get_entry_object(self):
        last_entry = self.request.session.pop("canopy_last_entry_id")
        if last_entry:
            try:
                obj = self.controller.entry_set.get(pk=last_entry)
            except Entry.DoesNotExist:
                return None
            else:
                return obj

    def get(self, request, *args, **kwargs):
        self.controller = self.get_controller_object()
        self.entry = self.get_entry_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["controller"] = self.controller
        kwargs["entry"] = self.entry

        return super().get_context_data(**kwargs)
