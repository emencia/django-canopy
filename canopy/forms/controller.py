from ..choices import get_controller_handler_order
from ..form_helpers import ControllerViewFormHelper
from ..models import Entry
from ..utils.loaders import get_handler_processor_class


class ControllerBaseForm:
    """
    Abstract form class for Canopy controller mechanics.

    It is intended to work along ``forms.Form``, meaning this abstract should be loaded
    after base form class.

    .. Note::
        Almost all internal methods are not intended to overwrite ``forms.Form``
        methods and are to be prefixed with an underscore to ensure they won't break
        some obscure ``forms.Form`` mechanic.

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

    def _process_handlers(self, entry):
        """
        Where we should process each controller handler with the entry (unsaved) object.

        TODO: Form clean should allow only for a single same handler type, like no
        duplicate of "save in db" and at least one handler is required.

        TODO: Handlers should have a priority, so the save in db one is probably the
        top one to avoid data loss on failure of other handlers.

        TODO: Walk through each related handler that is to be initialized and given
        the Entry object.
        """
        enabled = list(self.controller.get_handlers().values_list("name", flat=True))
        print("💄 Enabled handlers from controller:", enabled)
        for name in get_controller_handler_order():
            print("👷 Defined handler from setting:", name)
            if name in enabled:
                print("🚀 Processing entry with handler: {}".format(name))
                handler = get_handler_processor_class(name)()
                handler.proceed(entry)

        return

    def save(self, *args, commit=True, **kwargs):
        """
        Save request in a new Entry object.

        Entry object will be created with a relation to the Controller and will be
        marked with the current Controller version.

        Keyword Arguments:
            commit (boolean): If True the object is processed by handlers. Else the
            object is created but not processed, the object is still returned so you
            can process it latter. Default to True.

        Returns:
            Entry: Created Entry object.
        """
        created = Entry(
            controller=self.controller,
            version=self.controller.version,
            data=self._get_slot_datas(),
        )

        if commit is True:
             self._process_handlers(created)

        return created
