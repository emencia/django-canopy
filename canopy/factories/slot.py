import factory

from ..models import Slot

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
