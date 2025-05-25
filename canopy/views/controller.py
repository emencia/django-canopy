from django import forms
from django.conf import settings
from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin

from canopy.definitions.registry import get_registry
from ..models import Controller, Entry
from ..forms.forge import FormClassForge
from .mixins import AdminContext


registry = get_registry()


class ControllerFormView(FormView):
    """
    View to display a Controller form.
    """
    template_name_for_disabled = "canopy/controller/form/disabled.html"
    form_class = forms.Form  # Not used

    def get_template_names(self):
        """
        Template is determined from the object attribute ``form_template`` if controller
        is enabled else if it is disabled it will be the unique template from view
        attribute ``template_name_for_disabled``.
        """
        if self.object.enabled is not True:
            return [self.template_name_for_disabled]

        return [self.object.form_template]

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

    def response_when_disabled(self):
        """
        Return a specific response when controller is disabled.

        Either it returns a rendered response with a minimal context (just the
        controller object) on default or a Http404 response when settings
        ``CANOPY_CONTROLLER_EXCEPTION_WHEN_DISABLED`` is true.
        """
        if self.object.enabled is not True:
            if settings.CANOPY_CONTROLLER_EXCEPTION_WHEN_DISABLED is True:
                raise Http404(_("This form is disabled"))
            else:
                # We use a very minimal context to avoid performing any useless
                # operation
                return self.render_to_response({"controller": self.object})

    def get(self, request, *args, **kwargs):
        """
        Display blank form
        """
        self.object = self.get_object()

        disabled_response = self.response_when_disabled()

        return (
            disabled_response
            if disabled_response
            else self.render_to_response(self.get_context_data())
        )

    def post(self, request, *args, **kwargs):
        """
        Receive request and save or display errors.
        """
        self.object = self.get_object()

        disabled_response = self.response_when_disabled()
        if disabled_response:
            return disabled_response

        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form)


class ControllerSuccessView(TemplateView):
    """
    Basic template view to respond to form submit success.
    """
    template_name_for_disabled = "canopy/controller/success/disabled.html"

    def get_template_names(self):
        """
        Template is determined from the object attribute ``success_template`` if
        controller is enabled else if it is disabled it will be the unique template
        from view attribute ``template_name_for_disabled``.
        """
        if self.controller.enabled is not True:
            return [self.template_name_for_disabled]

        return [self.controller.success_template]

    def response_when_disabled(self):
        """
        Return a specific response when controller is disabled.

        Either it returns a rendered response with a minimal context (just the
        controller object) on default or a Http404 response when settings
        ``CANOPY_CONTROLLER_EXCEPTION_WHEN_DISABLED`` is true.
        """
        if self.controller.enabled is not True:
            if settings.CANOPY_CONTROLLER_EXCEPTION_WHEN_DISABLED is True:
                raise Http404(_("This form is disabled"))
            else:
                # We use a very minimal context to avoid performing any useless
                # operation
                return self.render_to_response({"controller": self.controller})

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
        last_entry = self.request.session.pop("canopy_last_entry_id", None)
        if last_entry:
            try:
                obj = self.controller.entry_set.get(pk=last_entry)
            except Entry.DoesNotExist:
                return None
            else:
                return obj

    def get(self, request, *args, **kwargs):
        self.controller = self.get_controller_object()

        disabled_response = self.response_when_disabled()
        if disabled_response:
            return disabled_response

        self.entry = self.get_entry_object()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["controller"] = self.controller
        kwargs["entry"] = self.entry

        return super().get_context_data(**kwargs)


class ControllerAdminDataVisualizerView(AdminContext, SingleObjectMixin, ListView):
    """
    Admin view to list Controller data entries structured according to the current
    Controller slot.
    """
    model = Controller
    template_name = "admin/canopy/controller/visualizer.html"
    http_method_names = ["get", "head", "options", "trace"]
    paginate_by = settings.CANOPY_ADMIN_CONTROLLER_DATA_PAGINATION

    def get_queryset(self):
        """
        Queryset to list controller entries
        """
        return self.object.get_data().values("id", "created", "data")

    def get_object(self):
        """
        Get the Category object for details
        """
        pk = self.kwargs.get("pk")

        try:
            obj = self.model.objects.filter(**{"id": pk}).get()
        except self.model.DoesNotExist:
            raise Http404(
                _("No {} found matching the query").format(
                    self.model._meta.verbose_name
                )
            )

        return obj

    def get_data_matrix(self):
        """
        Queryset to list controller entries
        """
        return {
            item["name"]: {
                "label": item["label"],
                "rendering": registry.get_definition(kind=item["kind"]).rendering,
            }
            for item in self.object.get_slots().values("label", "name", "kind")
        }

    def get_data_rows(self, matrix, data):
        """
        Build entry rows that match the matrix columns.

        Row columns are added in order, if a column match in row data it is rendered
        using the Slot rendering function else it will be None.
        """
        rows = []

        for entry in data:
            row = {"entry_id": entry["id"], "entry_created": entry["created"]}
            row.update({
                colname: (
                    colopts["rendering"](entry["data"][colname])
                    if colname in entry["data"]
                    else None
                )
                for colname, colopts in matrix.items()
            })
            rows.append(row)

        return rows

    def get_context_data(self, **kwargs):
        """
        Append specific admin context
        """
        context = super().get_context_data(**kwargs)

        matrix = self.get_data_matrix()

        context.update({
            "object": self.object,
            "data_matrix": matrix,
            "data_rows": self.get_data_rows(matrix, context["object_list"]),
            "title": _("Vizualize data for '%(title)s'") % {"title": self.object.title},
        })

        return context

    def get(self, request, *args, **kwargs):
        """
        Return HTML response with rendered content.
        """
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)
