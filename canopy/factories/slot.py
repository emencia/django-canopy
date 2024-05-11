import factory

from ..models import empty_fresh_dictionnary, Slot

from .controller import ControllerFactory


class SlotFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Slot model.
    """
    controller = factory.SubFactory(ControllerFactory)
    label = factory.Sequence(lambda n: "Slot {0}".format(n))
    name = factory.Sequence(lambda n: "slot_{0}".format(n))
    kind = "text-simple"
    required = False
    position = 0
    help_text = ""
    initial = ""

    class Meta:
        model = Slot

    @factory.lazy_attribute
    def field_options(self):
        """
        Return an initial fresh dictionnary.
        """
        return empty_fresh_dictionnary()

    @factory.lazy_attribute
    def widget_options(self):
        """
        Return an initial fresh dictionnary.
        """
        return empty_fresh_dictionnary()
