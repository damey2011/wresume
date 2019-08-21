from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from resumes.models import ContactFormData
from users.models import Client


def send_email_for_contact_form(sender, instance, created, **kwargs):
    if created:
        public_client = Client.objects.get(schema_name=settings.PUBLIC_SCHEMA_NAME)
        to_email = [instance.client.user.email]
        subject = 'New Wresu.me Contact Form Message'
        if public_client == instance.client:
            to_email = settings.ADMIN_EMAILS
            subject = '(HomePage)' + subject
        body = render_to_string('resumes/email/new-contact-form-fill.html', {'contact': instance})
        email = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, to_email)
        email.attach_alternative(body, 'text/html')
        email.send()


post_save.connect(send_email_for_contact_form, ContactFormData)
