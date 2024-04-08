from django.conf import settings

from ..models import Controller


class ControllerBaseForm:
    """
    TODO:
        Should be a simple abstract instead of a child of forms.Form so it is not tied
        to any form class and it can be inherited along a forms.Form or ModelForm to
        implement specific controller logic.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Save request object.
        """
        return
