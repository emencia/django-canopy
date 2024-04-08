import factory

from ..models import Entry

from .controller import ControllerFactory


class EntryFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Entry model.
    """
    controller = factory.SubFactory(ControllerFactory)
    data = "{}"

    class Meta:
        model = Entry

    @factory.lazy_attribute
    def version(self):
        """
        Get version from controller
        """
        return self.controller.version
