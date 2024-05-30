
def test_cached_initialized_registry():
    """
    Here we expect that registry has already been filled with test registry from the
    canopy AppConfig.
    """
    from canopy.definitions.registry import get_registry
    registry = get_registry()

    assert sorted(registry.names()) == ["boolean", "email", "text-simple", "textarea"]
