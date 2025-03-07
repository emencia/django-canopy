from django.urls import reverse

from canopy.factories import ControllerFactory, SlotFactory
from canopy.models import Controller
from canopy.utils.tests import html_pyquery


def test_view_detail(db, client, django_assert_num_queries):
    """
    Controller form view should contains all controller slot and a proper form
    structure.
    """
    controller = ControllerFactory()
    slot_text = SlotFactory(controller=controller, name="basic-text")
    url = reverse("canopy:controller-form", kwargs={"slug": controller.slug})

    with django_assert_num_queries(2):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)

    controller_form = dom.find("#controller-view")
    names = [
        item.get("name")
        for item in controller_form.find("input")
    ]

    assert names == ["csrfmiddlewaretoken", "basic-text", "submit-request-form"]


def test_view_success(db, client, django_assert_num_queries):
    """
    TODO: Should test valid submit send to the success page with data payload.
    """
    assert 1 == 42
