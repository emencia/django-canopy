from django import forms

from ..models import Slot

from .options import build_options_form


class SlotAdminInlineForm(forms.ModelForm):
    """
    Slot form for admin inline.
    """

    # TODO: This should be turned into a custom field that just display a link ?
    absolute_url = forms.DateField(required=False)

    class Meta:
        model = Slot
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("💚 Michou is here")

        #self.fields["absolute_url"] = forms.DateField(required=False)


class SlotAdminForm(forms.ModelForm):
    """
    Slot form for admin detail.
    """
    class Meta:
        model = Slot
        fields = "__all__"

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

    def clean(self):
        """
        Here we can alter data before save.

        Options values exists in cleaned_data at the same level than other Slot fields
        since we push them as slot form fields, not in field_options/widget_options.

        So here we could use registry to retrieve every option fields and dispatch them
        correctly in field_options/widget_options JSON.
        """
        cleaned_data = super().clean()

        if self.instance.id and "kind" in self.changed_data:
            cleaned_data["field_options"] = {}
            cleaned_data["widget_options"] = {}

        return cleaned_data
