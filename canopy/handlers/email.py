import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

from .. import __pkgname__
from ..exceptions import HandlerError

from .base import BaseHandler


class BaseSendEmailHandler(BaseHandler):
    """
    .. Todo::

        * Multipart body alternative (plain/text + html) is yet to be implemented;
        * Attachment is yet to be implemented;
        * Give site object to body context;
    """
    DEFAULT_SUBJECT = "[Site] Request"
    DEFAULT_PLAIN_TEMPLATE = "canopy/handlers/basic_email.txt"
    # DEFAULT_HTML_TEMPLATE = "canopy/handlers/basic_email.html"
    DEFAULT_RECIPIENTS = None
    DEFAULT_FROM = settings.DEFAULT_FROM_EMAIL
    SENDING_ERROR_FOR_USER = _(
        "An error occurred while sending the email. Please try again later."
    )
    SENDING_ERROR_FOR_LOGS = _("Request form mail sending failed")

    def get_subject(self, entry, **kwargs):
        return kwargs.get("subject", self.DEFAULT_SUBJECT)

    def get_senders(self, entry, **kwargs):
        return kwargs.get("from", self.DEFAULT_FROM)

    def get_recipients(self, entry, **kwargs):
        return kwargs.get("to", self.DEFAULT_RECIPIENTS)

    def get_plain_template(self, entry, **kwargs):
        return kwargs.get("plain_template", self.DEFAULT_PLAIN_TEMPLATE)

    def get_html_template(self, entry, **kwargs):
        return kwargs.get("html_template", self.DEFAULT_HTML_TEMPLATE)

    def get_email_object(self, entry, **kwargs):
        body = render_to_string(
            self.get_plain_template(entry, **kwargs),
            {
                # "site": site_object,
                "entry": entry,
            }
        )

        email = EmailMessage(
            subject=self.get_subject(entry, **kwargs),
            body=body,
            from_email=self.get_senders(entry, **kwargs),
            to=self.get_recipients(entry, **kwargs),
        )

        return email

    def proceed(self, entry, **kwargs):
        """
        Proceed to email sending.
        """
        print("🎨 BaseSendEmailHandler proceeding to send")

        logger = logging.getLogger(__pkgname__)
        email = self.get_email_object(entry, **kwargs)

        try:
            email.send(fail_silently=False)
            print(email.to)
            print("🌐 PIF")
        except SMTPException as err_smtp:
            # Not sure about this, in this current stage it will logs each time for all
            # mail handlers
            logger.error("{}: {}".format(LOG_ERROR, err_smtp))
            raise forms.ValidationError(USER_ERROR) from err_smtp
        except Exception as err:
            logger.error("{}: {}".format(LOG_ERROR, err))
            raise forms.ValidationError(USER_ERROR) from err


class SendEmailToStaffHandler(BaseSendEmailHandler):
    def get_recipients(self, entry, **kwargs):
        # In fact this would need a pre check on the setting, having it fail during
        # sending transaction is wrong behavior
        if not settings.ADMINS:
            raise HandlerError("SendEmailToStaffHandler: settings.ADMINS is empty")
        return [v for k, v in settings.ADMINS]


class SendEmailToWriterHandler(BaseSendEmailHandler):
    #def get_recipients(self, entry, **kwargs):
        #return []
    pass
