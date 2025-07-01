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
        skip_postgeneration_save = True

    @factory.lazy_attribute
    def form_template(self):
        return get_controller_form_template_default()

    @factory.lazy_attribute
    def success_template(self):
        return get_controller_success_template_default()

    @factory.post_generation
    def fill_handlers(self, create, extracted, **kwargs):
        """
        Add handlers.

        Arguments:
            create (bool): True for create strategy, False for build strategy.
            extracted (object): If a list assume it's a list of Handler names to add to
                the controller. Any other value will not add anything.
        """
        # Do nothing for build strategy
        if not create or not extracted or not isinstance(extracted, list):
            return

        # Import factory at this level to avoid circular import.
        from .handler import HandlerFactory

        # Add categories
        # TODO: Assert that each handler name exists from choices
        for handler in extracted:
            HandlerFactory(controller=self, name=handler)
