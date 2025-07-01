from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from ..models import Handler
from ..widgets import NonEditableLinkInput


class HandlerAdminInlineForm(forms.ModelForm):
    """
    Handler form for admin inline.
    """
    # Append a dummy field just to include Handler edition URL in inline list without to
    # to patch change view template.
    edit_url = forms.CharField(
        label=_("Edit"),
        required=False,
        widget=NonEditableLinkInput
    )

    class Meta:
        model = Handler
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fill 'edit_url' value with change view URL if there is a Handler instance given
        if kwargs.get("instance", None):
            self.fields["edit_url"].initial = reverse(
                "admin:canopy_handler_change",
                args=(kwargs["instance"].id,),
            )
        else:
            self.fields["edit_url"].initial = None


class HandlerAdminForm(forms.ModelForm):
    """
    Handler form for admin detail.
    """
    class Meta:
        model = Handler
        fields = "__all__"
