from django.forms.widgets import Input
from django.utils.translation import gettext_lazy as _


class NonEditableLinkInput(Input):
    """
    A dummy widget that has no input and just display a link from its field value.
    """
    input_type = "text"
    template_name = "canopy/widgets/non_editable_link.html"
