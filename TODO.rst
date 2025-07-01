
=====
Todos
=====

v0.3.3
*******

- [ ] Add controller data handler, at least the one to save in DB and the other one to
  send an email

  - [x] Model, forms, admin, factory;
  - [x] Controller would be able to select multiple handlers with a relation to each one;
  - [ ] Each ControllerHandler object should be able to carry some data, we may possibly
    use JSONField since handler options may vary from one to another;

    - [ ] Or finally use another FK to many object each of one for a parameter but this
      would need validation from a manifest;

  - [ ] First item of 'name' choices is never saved when selected from inline admin,
    all other items are well saved. Changing the order of choices always reproduce this
    bad behavior so this is not related to the handler name path. Once saved from the
    Handler change form it is retained from the inline form;

  - [ ] Process handler from Controller form save;
  - [ ] Handler should have a priority, these priorities should be defined from
    a setting. A dict of handler key -> priority number, if dict miss a handler, the
    default priority from its class attribute 'priority' would be used instead;


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

* We should have a way to have silent and automatically fill virtual fields.
  Like a field to store the IP adress from user request. The field would not be
  displayed but filled from form (it would need to be passed the Django request
  object).
* In a similar way we could have non field slot, like a HTML slot that would
  allow to insert HTML between fields but will be ignored from 'save()'.
