
=====
Todos
=====

v0.3.3
*******

* Add controller data handler, at least the one to save in DB and the other one to
  send an email;


Various
*******

* Some implemented slot kinds are not working yet (choices and file upload);
* Captchas kinds are missing;
* Permission per object on Controller to allow some user to manage specific forms and
  their slots;
* Plugin the Controller data export, it has been almost completed in code but it is not
  plugged in admin, actually only tests implements it;
* A form config export/import feature like from fobi. It would allow to quickly dump
  the Controller and its slots configurations in a file (JSON? YAML?) that can be used
  to load it and create a Controller with its slots, ready to go. Some config may not
  be loadable like the Controller name and slug that are unique;
* DjangoCMS plugin to include Controller form in a page;
* API
* A solution to draw form layout for each controller, crispy forms can not help for
  that since it can not be edited from admin, this is code only;
* Controller change view should include a safety check operation to ensure choices
  values (like handler), templates and its slots kinds are existing in current
  settings. Ever its an invisible automatic task from change view or it could be an
  optional task to manually trigger (from a click on a button in top actions);
* Choices from settings should be checked to be not empty during app initialization;
