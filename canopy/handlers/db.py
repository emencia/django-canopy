from ..models import Entry

from .base import BaseHandler


class SaveInDbHandler(BaseHandler):
    """
    Handler to save Entry object in database.
    """
    def proceed(self, entry, **kwargs):
        print("🎨 SaveInDbHandler proceeding to save")
        entry.save()

        return entry
