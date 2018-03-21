from django.conf import settings
from mail_templated import EmailMessage


class TemplatedEmail:

    def __init__(self, template_name, context, to, from_email=None, **kwargs):
        from_email = settings.EMAIL_FROM if from_email is None else from_email
        self.msg = EmailMessage(template_name, context, from_email, to, **kwargs)

    def send(self):
        if settings.ENABLE_NOTIFICATIONS is True and settings.EMAIL_ENABLED is True:
            self.msg.send()
