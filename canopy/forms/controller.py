from django.conf import settings

from ..models import Controller, Entry


class ControllerBaseForm:
    """
    Abstract form class for Canopy controller mechanics.

    It is intended to work along ``forms.Form``, means the abstract loads after it.

    TODO:
        We should have a way to have silent and automatically filled virtual fields.
        Like a field to store the IP adress from user request. The field would not be
        displayed but filled from form (it would need to be passed the Django request
        object).

        In a similar way we could have non field slot, like a HTML slot that would
        allow to insert HTML between fields but it is not taken in account from 'save()'

    Keyword Arguments:
        controller (Controller): Required Controller model object.
    """

    def __init__(self, *args, **kwargs):
        self.controller = kwargs.pop("controller", None)

        super().__init__(*args, **kwargs)

    def _get_slot_datas(self):
        """
        Collect all slot values to save as entry data.

        This requires that attribute ``cleaned_data``  has been correctly filled (like
        after the method ``clean()`` usage).

        Each slot data is named after its slot name not the field name, the latter is
        only used to get the value from ``cleaned_data``.

        Returns:
            dict: The dictionnary of slot values for the JSONfield.
        """
        return {
            name: self.cleaned_data.get(parameters["name"], None)
            for name, parameters in self.controller.fields_scheme.items()
        }

    def save(self, *args, commit=True, **kwargs):
        """
        Save request as an Entry object.

        Entry object will be created with a relation to the Controller and will be
        marked with the current Controller version.

        Keyword Arguments:
            commit (boolean): If True the object is saved in database. Else the
            instance is created but not saved, the object is still returned so you
            can save it latter. Default to True.

        Returns:
            Entry: Created Entry object.
        """
        created = Entry(
            controller=self.controller,
            version=self.controller.version,
            data=self._get_slot_datas(),
        )

        if commit is True:
            created.save()

        return created
