from ..form_helpers import ControllerViewFormHelper
from ..models import Entry


class ControllerBaseForm:
    """
    Abstract form class for Canopy controller mechanics.

    It is intended to work along ``forms.Form``, meaning this abstract should be loaded
    after base form class.

    .. Note::
        Almost all internal methods are not intended to overwrite ``forms.Form``
        methods and are to be prefixed with an underscore to ensure they won't break
        some obscure ``forms.Form`` mechanic.

    TODO:
        We should have a way to have silent and automatically fill virtual fields.
        Like a field to store the IP adress from user request. The field would not be
        displayed but filled from form (it would need to be passed the Django request
        object).

        In a similar way we could have non field slot, like a HTML slot that would
        allow to insert HTML between fields but will be ignored from 'save()'.

    Keyword Arguments:
        controller (Controller): Required Controller model object. Not that a form built
            from forge will already have the ``controller`` set as attribute, however
            you may override it there for some specific purpose (like testing).
    """

    def __init__(self, *args, **kwargs):
        # Try to get Controller object from argument if it has not already been set
        # from forge
        try:
            self.controller = kwargs.pop("controller")
        except KeyError:
            pass

        # Validate we have a controller finally
        if not getattr(self, "controller", None):
            raise KeyError(
                "Controller form requires a Controller object to be given as a non "
                "positional argument (eg: 'controller=my_controller')."
            )

        super().__init__(*args, **kwargs)

        self.helper = ControllerViewFormHelper()

    def _get_slot_datas(self):
        """
        Collect all slot values to save as entry data.

        This requires that attribute ``cleaned_data``  has been correctly filled (like
        after the method ``clean()`` usage).

        Returns:
            dict: The dictionnary of slot values for the JSONfield.
        """
        return {
            name: self.cleaned_data.get(name, None)
            for name in self.controller.get_slots().values_list("name", flat=True)
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
