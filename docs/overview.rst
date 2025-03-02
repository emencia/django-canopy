
========
Overview
========

.. Warning::
    This is a temporary document.

Goal
****

The goal of Canopy is to allow to dynamically create forms from admin instead of
coding them. We call these forms *Controllers*.

Controller
**********

A controller can contains various fields called *Slots* because it is intended
to be also non fields like HTML to insert between two fields.

Slot
****

A slot defines the input type or content it will bind into form and its possible
options, this is defined by the slot *kind*.

We define all available kinds in *definitions* that are loaded on application init in
definition registry.

So the slot kinds determine what definition to assign to the slot that will dict what
input field it will display in form and its options.

Definitions
***********

A kind definition defines Django field to use and its options. Definition field options
defines the Django field to use in Slot form to manage the options values.

For exemple, a slot with kind ``text-simple`` determine a Django field
``forms.CharField`` to manage the slot value in the controller form. However a
CharField have some options like maximum value length or strip option. To allow user
to define these options, the definition defines what Django fields will be used in
the Slot form to manage these options.

Technically, in the admin the Slot form is enhanced to inject these options fields that
we can call *virtual field* since they are not part of the Slot model.

