from .models import Entry


class SaveInDbHandler:
    def __init__(self, *args, **kwargs):
        pass

    def proceed(self, controller, data, **kwargs):
        created = Entry(
            controller=controller,
            version=controller.version,
            data=data,
        )
