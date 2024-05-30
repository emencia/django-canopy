from django import forms

from ..models import Slot

from .options import build_options_form


class SlotAdminForm(forms.ModelForm):
    """
    Slot form for admin.

    NOTE:

    * The slot form will have to watch for "kind" change since changing to another
      kind means to reset 'field_options' and 'widget_options';
    * There is currently no clean method since options fields are naturally validated;

    """

    def __init__(self, *args, **kwargs):
        field_options_formclass = build_options_form(
            "field",
            slot=kwargs.get("instance"),
        )
        widget_options_formclass = build_options_form(
            "widget",
            slot=kwargs.get("instance"),
        )
        self.field_options_form = field_options_formclass(prefix="field_opts")
        self.widget_options_form = widget_options_formclass(prefix="widget_opts")

        super().__init__(*args, **kwargs)

        # Widget are not merged yet
        self.fields.update({
            name: field
            for name, field in self.field_options_form.fields.items()
        })

        # Hide field_options and widget_options fields
        # TODO: Disabled for now, we want to still see them as unreadable during
        # development to control their value
        # self.fields["field_options"].widget = forms.HiddenInput()
        # self.fields["widget_options"].widget = forms.HiddenInput()

    class Meta:
        model = Slot
        fields = "__all__"
