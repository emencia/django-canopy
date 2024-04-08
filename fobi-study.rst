Fobi replacement study
======================

Goal is to make dynamical forms alike Fobi so we can drop it.

Introduction
************

Resume
------

* Controller model represent a form controller;
* Controller model holds Slots;
* Slot model represent a field (and possibly further other kind like buttons or text);
* Controller form will save a valid data submit into an Entry;
* Entry model store the user submitted data;


Technically
-----------

* Controller form object is built on the go;
* Since of dynamical nature of Controller form, Entry define a generic column structure
  where the data is stored in a JSON field;
* Slot kinds will be a set of slot pre definition which defines field options and also
  stuff for crispy helper and how to manage data;


Unstable form data structure
****************************

Problematics
------------

Since user submitted data is stored as JSON and Entry model is a generic holder for
many various controllers, how to manage stored data when controller is modified ?

Example: a Controller which have A and B fields, some user submitted data has already
been stored but then controller is modified to remove A field and include a new
one C ?

Then what if further a field A is added again but with different kind or
goal ?

The Fobi way
------------

First, this is managed from "contrib handler", since cleaned data is managed from these
handlers, like email sender handler or db store handler.

The stored data by db store handler is never altered or updated when data structure is
changed from a form field change. The data stay unchanged, each data entry (cleaned
data from a form submission) includes the data structure as "headers" that help to
render them (for export or listing).

Data entries are rendered using the current form data structure, unknowed field from
current data structure are ignored and missing fields are probably filled blank with
field default value.

Plan A
------

We do just as Fobi does. This is simple and working. Also it is innefficient in
db storage size since we would store many data with more fields and values than a
current state form. It may also making it difficult to exploit data programmatically
from another app.

As a simple patch for this we could provide a way to "restructurate" all datas, the
most probably with a dedicated Django command.

Finally the form should have an automatic version to increment on any structure change.
And each entry would be saved with the form version used. This could help a little to
"restructurate" operations to avoid opening entry which won't need it, but not so much.

Plan B
------

Use a keydb (like reddis) to store data, it is efficient as a db but does not have
constraint on data structure.

This won't be done since it would requires to depend from a keydb install on system. We
do not want that.

Plan C
------

Restructurate each data entry on each form data structure change. This keep data
integrity at the best and avoid too much logic when rendering.

This won't be done because it would take lot of ressources on forms that already have
many data. The restructurate thing is something to keep ad hoc and on manual action.


Translations
************

Problematics
------------

How to implement and manage title/label/etc.. translations ?
