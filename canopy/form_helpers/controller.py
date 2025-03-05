from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Submit

from .base import BaseFormHelper


class ControllerViewFormHelper(BaseFormHelper):
    """
    Automatic helper for Controller view
    """
    DEFAULT_CSSID = "controller-view"
    DEFAULT_CSSCLASSES = "needs-validation"
    DEFAULT_INPUTS = [
        Submit("submit-request-form", _("Submit")),
    ]
