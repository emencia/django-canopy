from itertools import chain

from canopy.definitions.registry import get_registry
registry = get_registry()


class DummyKind:
    """
    Dummy Kind object for dummy rendering.

    Used internally for data columns that does not have a related Slot and Kind.
    """
    def rendering(self, value):
        return str(value)


class BaseExporter:
    """
    Export all Entry objects.

    Base exporter only export a Python dictionnary of computed Entry objects.
    """
    def __init__(self, registry, default_kind=None):
        self.registry = registry
        self.default_kind = default_kind or DummyKind()

    def render_for_kind(self, kind, value):
        """
        Return rendered value for given Kind object.
        """
        return kind.rendering(value)

    def render_for_slot(self, slot, value):
        """
        Return rendered value for given Slot object.
        """
        kind = self.registry.get_definition(slot.kind)

        return self.render_for_kind(kind, value)

    def get_matrix(self, slots, data):
        """
        Compile headers for all data and slots.

        A data column is assumed to be deprecated when it does not have corresponding
        Slot (match from its Slot name).

        Deprecated columns are added after the other ones and Slot order should be
        respected.

        .. Note::
            This solution does not allow for pagination since from a set of results to
            another (from a page to another one) the data slot columns may differ and it
            would lead to different tables.

        Returns:
            dict: A dictionnary of all possible columns from all entries data and slots.
                This is guaranteed to fit all entries data.
        """
        headers = {
            slot["name"]: {
                "label": slot["label"],
                "in_slots": True,
                "in_data": False,
                "rendering": registry.get_definition(kind=slot["kind"]).rendering,
            }
            for slot in slots.values("label", "name", "kind")
        }

        # Merge all data columns without duplicates and preserving order (of the first
        # occurence of an item)
        combined_columns = list(
            dict.fromkeys(chain(*[entry.keys() for entry in data]))
        )

        # Update headers to add deprecated columns and update existing ones to mark them
        for name in combined_columns:
            if name not in headers:
                # Deprecated column is not in Slots
                headers[name] = {
                    "label": name,
                    "in_slots": False,
                    "in_data": True,
                    "rendering": self.default_kind.rendering,
                }
            else:
                # Column exists in Slots
                headers[name]["in_data"] = True

        return headers

    def build_rows(self, matrix, data):
        """
        Build rows for data structured from given matrix.
        """
        for rowid, rowdata in data:
            yield [
                colopts["rendering"](rowdata[colname]) if colname in rowdata else None
                for colname, colopts in matrix.items()
            ]

    def export(self, controller):
        data_queryset = controller.get_data()

        matrix = self.get_matrix(
            controller.get_slots(),
            data_queryset.values_list("data", flat=True)
        )

        return {
            "data_matrix": matrix,
            "data_rows": self.build_rows(
                matrix,
                data_queryset.values_list("id", "data")
            ),
        }
