from django.db import models
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class BaseEmailInstance(object):

    def __init__(self, obj, subject=None,
            body=None, to=None, cc=None, bcc=None, from_email=None,
            attachments=None, **kwargs):
        self.object = obj
        self.subject = subject or getattr(self, 'SUBJECT', None)
        self.body = body
        self.to = to
        self.cc = cc
        self.bcc = bcc or getattr(self, 'BCC', None)
        self.from_email = from_email or getattr(self, 'FROM_EMAIL', None)
        self.attachments = attachments
        self.kwargs = kwargs

    def get_subject(self):
        return self.subject or unicode(self.object)

    def get_body(self):
        return self.body

    def get_from_email(self):
        if not self.from_email:
            return settings.DEFAULT_FROM_EMAIL
        return self.from_email

    def get_attachments(self):
        return self.attachments

    def get_to(self):
        return self.to

    def get_bcc(self):
        return self.bcc

    def get_cc(self):
        return self.cc

    def get_message(self):
        msg = EmailMultiAlternatives(
                self.get_subject(),
                self.get_body(),
                self.get_from_email(),
                to=self.get_to(),
                bcc=self.get_bcc(),
                cc=self.get_cc(),
                attachments=self.get_attachments(),
                )
        return msg

    def send(self):
        return self.get_message().send()


class BaseMultipartEmail(BaseEmailInstance):

    def get_html_body(self):
        raise ImproperlyConfigured("%(cls)s is missing a HTML body. Override "
                "%(cls)s.get_html_body, " % {
                    'cls': self.__class__.__name__
                    })

    def get_message(self):
        msg = super(BaseMultipartEmail, self).get_message()
        html_body = self.get_html_body()
        msg.attach_alternative(html_body, "text/html")
        return msg


class TemplateEmailMixin(object):
    template_name_suffix = ''
    template_name = None

    def get_template_names(self):
        """
        Return a list of template names to be used.
        Returns the following list:

        * the value of ``template_name`` (if provided)
        * <app>/emails/<model><template_name_suffix>.html
        * send_instance/email/default.html
        """
        names = []
        if self.template_name:
            names.append(self.template_name)

        if isinstance(self.object, models.Model):
            names.append("%s/emails/%s%s.html" % (
                self.object._meta.app_label,
                self.object._meta.object_name.lower(),
                self.template_name_suffix
            ))

        #default template
        names.append('send_instance/email/default.html')

        return names

    def get_context_data(self, **kwargs):
        context = kwargs
        context['object'] = self.object
        return context

    def render(self):
        """
        ``kwargs`` will be passed as ``params`` to the template context.
        """
        rendered = render_to_string(
                self.get_template_names(),
                self.get_context_data(**self.kwargs)
                )
        return rendered


class TemplateEmail(TemplateEmailMixin, BaseMultipartEmail):
    """
    Provide HTML/plain text mail from template for given model instance.
    """

    def get_html_body(self):
        return self.render()

    def get_body(self):
        html_body = self.render()
        return strip_tags(html_body)
