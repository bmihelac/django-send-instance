====================
django-send-instance
====================

django-send-instance makes easy to send Django model instances.

Examples::

    # create book instance
    book = Book.objects.create(
            name='Sample book',
            author_email='test@example.com',
            )

    from send_instance.email import TemplateEmail
    TemplateEmail(self.book, to=[self.book.author_email]).send()

This will send HTML and plain text mail, consisting of all instance fields and
values.

Template ``<app>/emails/<model><template_name_suffix>.html`` will be used if 
exists to render email content.
