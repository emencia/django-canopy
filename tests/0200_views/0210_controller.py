from django.urls import reverse

import pytest

from canopy.factories import ControllerFactory, SlotFactory
from canopy.utils.tests import html_pyquery


def test_view_detail(db, client, django_assert_num_queries):
    """
    Controller form view should contains all controller slot and a proper form
    structure.
    """
    controller = ControllerFactory()
    SlotFactory(controller=controller, name="basic-text")
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


@pytest.mark.skip("We need implementation of payload passing from form to success")
def test_view_success(db, client):
    """
    TODO: Should test valid submit send to the success page with data payload.
    """
    controller = ControllerFactory()
    SlotFactory(controller=controller, name="basic-text")
    url = reverse("canopy:controller-form", kwargs={"slug": controller.slug})

    response = client.post(url, data={"basic-text": "Foo"}, follow=True)

    assert response.redirect_chain == [
        (reverse("canopy:controller-success"), 302),
    ]
    assert response.status_code == 200

    assert 1 == 42
