import factory

from ..models import Controller
from ..choices import (
    get_controller_form_template_default, get_controller_success_template_default,
)


class ControllerFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Controller model.
    """
    title = factory.Sequence(lambda n: "Controller {0}".format(n))
    slug = factory.Sequence(lambda n: "controller-{0}".format(n))
    enabled = True
    version = 0

    class Meta:
        model = Controller

    @factory.lazy_attribute
    def form_template(self):
        return get_controller_form_template_default()

    @factory.lazy_attribute
    def success_template(self):
        return get_controller_success_template_default()
