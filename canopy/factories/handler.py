import factory

from ..choices import get_controller_handler_default
from ..models import Handler

from .controller import ControllerFactory


class HandlerFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Handler model.
    """
    controller = factory.SubFactory(ControllerFactory)

    class Meta:
        model = Handler

    @factory.lazy_attribute
    def name(self):
        """
        Return the default handler choice value.
        """
        return get_controller_handler_default()
