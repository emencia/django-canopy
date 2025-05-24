from canopy.definitions import DefinitionsRegistry
from canopy.factories import ControllerFactory, EntryFactory, SlotFactory
from canopy.export import DummyKind, BaseExporter


def test_render_for_kind():
    """
    Render a data value according to its related Kind
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    kind = registry.get_definition("text-simple")

    exporter = BaseExporter(registry)
    assert exporter.render_for_kind(kind, "Hello world!") == "Hello world!"
    assert exporter.render_for_kind(kind, 42.000) == "42.0"
    assert exporter.render_for_kind(kind, ["plip"]) == "['plip']"


def test_render_for_slot():
    """
    Render a data value according to its related Slot
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    text = SlotFactory.build(label="Foo", name="foo", kind="text-simple")

    exporter = BaseExporter(registry)
    assert exporter.render_for_slot(text, "Hello world!") == "Hello world!"
    assert exporter.render_for_slot(text, 42.000) == "42.0"
    assert exporter.render_for_slot(text, ["plip"]) == "['plip']"


def test_get_matrix(db):
    """
    Method should build the correct matrix from given slots and data
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    ctrl = ControllerFactory()
    SlotFactory(controller=ctrl, kind="text-simple", label="Name", name="name")
    SlotFactory(controller=ctrl, kind="textarea", label="Comment", name="comment")
    SlotFactory(controller=ctrl, kind="choice-list", label="Hobbies", name="hobbies")

    data = [
        # One slot is missing
        {
            "name": "Jimmy",
            "comment": "Hey joe!",
        },
        # Two slots missing and a deprecated one
        {
            "deprecated": "ollymolly",
            "name": "Billy",
        },
        # All slots with a deprecated one
        {
            "niet": "key",
            "name": "Franky",
            "comment": "Relax",
            "deprecated": "ollymolly",
        },
        # No any slot and a single deprecated
        {
            "useless": "nope",
        },
    ]

    default_kind = DummyKind()

    exporter = BaseExporter(registry, default_kind=default_kind)

    matrix = exporter.get_matrix(ctrl.get_slots(), data)

    # print()
    # print("matrix:", json.dumps(matrix, indent=4, cls=ExtendedJsonEncoder))

    assert matrix == {
        "name": {
            "label": "Name",
            "in_slots": True,
            "in_data": True,
            "rendering": str,
        },
        "comment": {
            "label": "Comment",
            "in_slots": True,
            "in_data": True,
            "rendering": str,
        },
        "hobbies": {
            "label": "Hobbies",
            "in_slots": True,
            "in_data": False,
            "rendering": str,
        },
        "deprecated": {
            "label": "deprecated",
            "in_slots": False,
            "in_data": True,
            "rendering": default_kind.rendering,
        },
        "niet": {
            "label": "niet",
            "in_slots": False,
            "in_data": True,
            "rendering": default_kind.rendering,
        },
        "useless": {
            "label": "useless",
            "in_slots": False,
            "in_data": True,
            "rendering": default_kind.rendering,
        }
    }


def test_build_rows_entries_data(db):
    """
    Method should build row for each entry data where data columns are aligned with
    the matrix ones.
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

    data_queryset = ctrl.get_data()
    exporter = BaseExporter(registry)

    matrix = exporter.get_matrix(
        ctrl.get_slots(),
        data_queryset.values_list("data", flat=True)
    )
    rows = exporter.build_rows(matrix, data_queryset.values_list("id", "data"))

    # print()
    # print("matrix:", json.dumps(list(rows), indent=4, cls=ExtendedJsonEncoder))

    assert list(rows) == [
        [None, "Hey joe!", "Jimmy", None, None, None],
        [None, None, "Billy", "ollymolly", None, None],
        [None, "Relax", "Franky", "ollymolly", "key", None],
        [None, None, None, None, None, "nope"],
    ]


def test_export(db):
    """
    Exporter should build a Python object for the Controller data according to the
    matrix.
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

    default_kind = DummyKind()

    exporter = BaseExporter(registry, default_kind=default_kind)
    exported = exporter.export(ctrl)
    assert "data_matrix" in exported
    assert "data_rows" in exported

    assert exported["data_matrix"] == {
        "name": {
            "label": "Name",
            "in_slots": True,
            "in_data": True,
            "rendering": str,
        },
        "comment": {
            "label": "Comment",
            "in_slots": True,
            "in_data": True,
            "rendering": str,
        },
        "hobbies": {
            "label": "Hobbies",
            "in_slots": True,
            "in_data": False,
            "rendering": str,
        },
        "deprecated": {
            "label": "deprecated",
            "in_slots": False,
            "in_data": True,
            "rendering": default_kind.rendering,
        },
        "niet": {
            "label": "niet",
            "in_slots": False,
            "in_data": True,
            "rendering": default_kind.rendering,
        },
        "useless": {
            "label": "useless",
            "in_slots": False,
            "in_data": True,
            "rendering": default_kind.rendering,
        }
    }

    assert list(exported["data_rows"]) == [
        [None, "Hey joe!", "Jimmy", None, None, None],
        [None, None, "Billy", "ollymolly", None, None],
        [None, "Relax", "Franky", "ollymolly", "key", None],
        [None, None, None, None, None, "nope"],
    ]
