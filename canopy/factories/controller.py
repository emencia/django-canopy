import factory

from ..models import Controller


class ControllerFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Controller model.
    """
    title = factory.Sequence(lambda n: "Controller {0}".format(n))
    slug = factory.Sequence(lambda n: "controller-{0}".format(n))
    version = 1

    class Meta:
        model = Controller
