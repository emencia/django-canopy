
def test_cached_initialized_registry():
    """
    Ensure loaded registry is working well
    """
    from canopy.definitions.registry import get_registry
    registry = get_registry()

    assert sorted(registry.names()) == ["boolean", "email", "text-simple", "textarea"]
