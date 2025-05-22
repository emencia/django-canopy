from canopy.utils.tests import html_pyquery

from canopy.definitions import DefinitionsRegistry
from canopy.factories import ControllerFactory, EntryFactory, SlotFactory
from canopy.export import HtmlExporter


def test_export(db):
    """
    HTML exporter should build a table for listed data.
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

    EntryFactory(
        controller=ctrl,
        data={
            "name": "Jimmy",
            "comment": "Hey joe!",
        }
    )
    EntryFactory(
        controller=ctrl,
        data={
            "name": "Billy",
            "deprecated": "ollymolly",
        }
    )
    EntryFactory(
        controller=ctrl,
        data={
            "niet": "key",
            "name": "Franky",
            "comment": "Relax",
            "deprecated": "ollymolly",
        }
    )
    EntryFactory(
        controller=ctrl,
        data={
            "useless": "nope",
        }
    )

    renderer = HtmlExporter(registry)
    rendered = renderer.export(ctrl)
    dom = html_pyquery(rendered)

    headers = [v.text for v in dom.find("thead th")]
    assert headers == ["hobbies", "comment", "name", "deprecated", "niet", "useless"]

    rows = [
        [cell.text for cell in row.cssselect("td")]
        for row in dom.find("tbody tr")
    ]
    assert rows == [
        ["None", "Hey joe!", "Jimmy", "None", "None", "None"],
        ["None", "None", "Billy", "ollymolly", "None", "None"],
        ["None", "Relax", "Franky", "ollymolly", "key", "None"],
        ["None", "None", "None", "None", "None", "nope"],
    ]
