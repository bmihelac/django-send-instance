from pathlib import Path
from django.test import override_settings

from django.conf import settings
from django.core import mail
from django.test import TestCase

from send_instance.email import TemplateEmail

from .models import Book


class BookEmail(TemplateEmail):
    def get_to(self):
        return [self.object.author_email]

    def get_subject(self):
        return "New book added"


class TemplateEmailTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            name="Sample book",
            author_email="test@example.com",
        )

    def test_default_subject(self):
        email = TemplateEmail(self.book)
        self.assertEqual(email.get_subject(), str(self.book))

    def test_default_template(self):
        TemplateEmail(self.book, to=[self.book.author_email]).send()
        expected = (
            "ID: %s\nBook name: Sample book\nAuthor email: test@example.com"
            % self.book.id
        )
        self.assertIn(expected, mail.outbox[0].body)

    def test_custom_template(self):
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                "DIRS": [Path(__file__).parent.parent / "templates"],
                'APP_DIRS': True,
            }
        ]
        with override_settings(TEMPLATES=TEMPLATES):
            TemplateEmail(self.book, to=[self.book.author_email]).send()
            expected = "Book %s has been added." % self.book.name
            self.assertIn(expected, mail.outbox[0].body)

    def test_override_class(self):
        BookEmail(self.book).send()
        self.assertEquals(mail.outbox[0].subject, "New book added")
        self.assertEquals(mail.outbox[0].to, [self.book.author_email])
