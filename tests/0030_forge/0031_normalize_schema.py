#from canopy.forms.forge import FormClassForge
#from canopy.factories import ControllerFactory, SlotFactory
#from canopy.models import empty_fresh_dictionnary


#def test_normalize_to_schema_from_dict():
    #"""
    #Method 'normalize_to_schema' should return a slot schema from a dict.

    #NOTE: Given dict is already a proper schema so there is nothing different to expect.
    #"""
    #assert FormClassForge().normalize_to_schema({
        #"foo": {
            #"kind": "text-simple",
            #"label": "Foo",
            #"name": "foo",
            #"required": False,
            #"position": 1,
            #"help_text": "",
            #"initial": ""
        #},
    #}) == {
        #"foo": {
            #"kind": "text-simple",
            #"label": "Foo",
            #"name": "foo",
            #"required": False,
            #"position": 1,
            #"help_text": "",
            #"initial": ""
        #},
    #}


#def test_normalize_to_schema_from_iterable():
    #"""
    #Method 'normalize_to_schema' should return a slot schema from an iterable.
    #"""
    #assert FormClassForge().normalize_to_schema((
        #(
            #"foo", {
                #"kind": "text-simple",
                #"label": "Foo",
                #"name": "foo",
                #"required": False,
                #"position": 1,
                #"help_text": "",
                #"initial": ""
            #},
        #),
    #)) == {
        #"foo": {
            #"kind": "text-simple",
            #"label": "Foo",
            #"name": "foo",
            #"required": False,
            #"position": 1,
            #"help_text": "",
            #"initial": ""
        #},
    #}


#def test_normalize_to_schema_from_controller(db):
    #"""
    #Method 'normalize_to_schema' returns a slot schema from Controller object.
    #"""
    ## Create a controller object with some slot objectss
    #controller = ControllerFactory()
    #SlotFactory(label="Foo", name="foo", controller=controller, position=1)
    #SlotFactory(label="Bar", name="bar", controller=controller, position=2)

    #assert FormClassForge().normalize_to_schema(controller) == {
        #"foo": {
            #"kind": "text-simple",
            #"label": "Foo",
            #"name": "foo",
            #"required": False,
            #"position": 1,
            #"help_text": "",
            #"initial": "",
            #"field_options": empty_fresh_dictionnary(),
            #"widget_options": empty_fresh_dictionnary(),
        #},
        #"bar": {
            #"kind": "text-simple",
            #"label": "Bar",
            #"name": "bar",
            #"required": False,
            #"position": 2,
            #"help_text": "",
            #"initial": "",
            #"field_options": empty_fresh_dictionnary(),
            #"widget_options": empty_fresh_dictionnary(),
        #}
    #}
