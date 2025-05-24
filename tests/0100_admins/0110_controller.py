import datetime
from zoneinfo import ZoneInfo

from freezegun import freeze_time

from django.urls import reverse

from canopy.factories import ControllerFactory, EntryFactory, SlotFactory
from canopy.models import Controller
from canopy.utils.tests import (
    get_admin_add_url, get_admin_change_url, get_admin_list_url,
)
from canopy.definitions import DefinitionsRegistry
from canopy.utils.tests import html_pyquery


def test_admin_ping_add(db, admin_client):
    """
    Controller model admin add form view should not raise error on GET request.
    """
    url = get_admin_add_url(Controller)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_admin_ping_list(db, admin_client):
    """
    Controller model admin list view should not raise error on GET request.
    """
    url = get_admin_list_url(Controller)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_admin_ping_detail(db, admin_client):
    """
    Controller model admin detail view should not raise error on GET request.
    """
    obj = ControllerFactory()

    url = get_admin_change_url(obj)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


@freeze_time("2012-10-15 10:00:00")
def test_admin_visualizer(db, admin_client, django_assert_num_queries):
    """
    TODO
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    ctrl = ControllerFactory()
    SlotFactory(
        controller=ctrl, kind="text-simple", label="Name", name="name", position=2
    )
    SlotFactory(
        controller=ctrl, kind="textarea", label="Comment", name="comment", position=1
    )
    SlotFactory(
        controller=ctrl, kind="choice-list", label="Hobbies", name="hobbies", position=0
    )

    jimmy = EntryFactory(
        controller=ctrl,
        data={
            "name": "Jimmy",
            "comment": "Hey joe!",
        }
    )
    billy = EntryFactory(
        controller=ctrl,
        data={
            "name": "Billy",
            "deprecated": "ollymolly",
        }
    )
    nope = EntryFactory(
        controller=ctrl,
        data={
            "useless": "nope",
        }
    )
    homer = EntryFactory(
        controller=ctrl,
        data={
            "name": "Homer",
            "comment": "Doh",
            "hobbies": "Eating",
        }
    )
    EntryFactory(
        controller=ctrl,
        data={
            "name": "Bart",
            "comment": "Cowabunga",
            "hobbies": "Disturbing",
        }
    )
    franky = EntryFactory(
        controller=ctrl,
        data={
            "niet": "key",
            "name": "Franky",
            "comment": "Relax",
            "deprecated": "ollymolly",
        }
    )
    # Enforce a different date to check about list ordering
    franky.created = datetime.datetime(2012, 10, 14, 10, 0).replace(
        tzinfo=ZoneInfo("UTC")
    )
    franky.save()

    url = reverse("admin:canopy_controller_data_visualizer", kwargs={"pk": ctrl.id})
    response = admin_client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)

    headers = [v.text for v in dom.find("#canopy-controller-data thead th .text *")]
    assert headers == ["ID", "Created", "Hobbies", "Comment", "Name"]

    rows = [
        [cell.text for cell in row.cssselect("td *")]
        for row in dom.find("tbody tr")
    ]
    assert rows == [
        [str(franky.id), "Oct. 14, 2012, 5 a.m.", "-", "Relax", "Franky"],
        [str(jimmy.id), "Oct. 15, 2012, 5 a.m.", "-", "Hey joe!", "Jimmy"],
        [str(billy.id), "Oct. 15, 2012, 5 a.m.", "-", "-", "Billy"],
        [str(nope.id), "Oct. 15, 2012, 5 a.m.", "-", "-", "-"],
        [str(homer.id), "Oct. 15, 2012, 5 a.m.", "Eating", "Doh", "Homer"],
    ]

    assert len(dom.find(".paginator a, .paginator span")) == 2
