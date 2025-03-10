
def test_cached_initialized_registry():
    """
    Ensure loaded registry is working well
    """
    from canopy.definitions.registry import get_registry
    registry = get_registry()

    assert sorted(registry.names()) == [
        "boolean",
        "choice-list",
        "choice-radio",
        "date",
        "datetime",
        "decimal",
        "email",
        "file",
        "integer",
        "ip-address",
        "ip4-address",
        "ip6-address",
        "multiple-choice-checkbox",
        "multiple-choice-list",
        "text-simple",
        "textarea",
        "time",
    ]
