
=========
Changelog
=========

Development
***********

TODO


Version 0.3.1 - 2025/03/11
**************************

* Added many more Kind definitions to cover the basic useful Django form fields;
* Continued test coverage improvements;
* Cleaned some useless Forge and Registry methods;
* Changed form view so it store the created Entry ID in session;
* Improved success view so it knows about its related Controller and Entry;


Version 0.3.0 - 2025/03/05
**************************

* Refactored Slot definition with Pydantic's dataclasses;
* Adapted Controller form view to the new registry;
* Removed CMS from sandbox requirements;
* Added Slot inlines with sortable2 in Controller admin details;
* Added Crispy forms to requirements with a basic form helper for Controller form view;
* Added encoder 'DjangoJSONEncoder' to 'Controller.version';
* Upgraded development requirements;
* Upgraded frontend requirements;
* Added logo;


Version 0.2.0 - Unreleased
**************************

* The controller form save is now working with basic fields;
* Added working basic controller form;
* Added model admins;
* Refactored registry;


Version 0.1.0 - Unreleased
**************************

Initial version started to prototype application with starting models, form forge,
dummy base controller form and some tests.
