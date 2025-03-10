from django.urls import reverse

from canopy.factories import ControllerFactory, SlotFactory
from canopy.utils.tests import html_pyquery


def test_view_detail_detail(db, client, django_assert_num_queries):
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


def test_view_detail_post(db, client, django_assert_num_queries):
    """
    Controller form should redirect to success view when submitted data have been
    validated. And the success view should retrieve the related controller and entry
    objects.
    """
    controller = ControllerFactory()
    SlotFactory(controller=controller, name="basic-text", required=True)

    form_url = reverse("canopy:controller-form", kwargs={"slug": controller.slug})
    success_url = reverse("canopy:controller-success", kwargs={"slug": controller.slug})

    # Without required data, form is invalid and return to itself
    with django_assert_num_queries(2):
        response = client.post(form_url, data={}, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    # With required data, form is valid and goes to success
    # NOTE: This involves two suite of querysets, the ones from form view then the ones
    # from the success view
    # with django_assert_num_queries(16) as captured_queries:
    response = client.post(form_url, data={"basic-text": "Foo"}, follow=True)

    # import json
    # print(json.dumps(list(captured_queries), indent=4))
    # selection_queries = [
    #     q["sql"].replace('\"', "")
    #     for q in captured_queries
    #     if q["sql"].startswith("SELECT")
    # ]
    # print()
    # print(json.dumps(selection_queries, indent=4))
    # assert 1 == 42
    assert response.redirect_chain == [(success_url, 302),]
    assert response.status_code == 200
    # Success view has retrieved related Controller object
    assert response.context["controller"].id == controller.id
    # Since succeeded, created Entry object has been retrieved from stored id in session
    assert response.context.get("entry").id == 1
