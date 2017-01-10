====================
django-send-instance
====================

django-send-instance makes it easy to send Django model instances.

Installation and configuration
------------------------------

    $ pip install -e git+https://github.com/bmihelac/django-send-instance.git#egg=django-send-instance

You need to add it to your ``INSTALLED_APPS``:

.. code-block:: python

    # settings.py
    INSTALLED_APPS = (
        ...
        'send-instance',
    )
    
Usage
-----

Examples::

    # create book instance
    book = Book.objects.create(
            name='Sample book',
            author_email='test@example.com',
            )

    from send_instance.email import TemplateEmail
    TemplateEmail(self.book, to=[self.book.author_email]).send()

This will send HTML and plain text multipart email,
consisting of all instance fields and values::

    Content-Type: multipart/alternative; boundary="===============1662479169=="
    MIME-Version: 1.0
    Subject: Sample book
    From: webmaster@localhost
    To: test@example.com
    Date: Wed, 15 Aug 2012 11:24:21 -0000
    Message-ID: <20120815112421.75291.76544@myhost.local>

    --===============1662479169==
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit


    ID: 1
    Book name: Sample book
    Author email: test@example.com



    --===============1662479169==
    Content-Type: text/html; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit


    <label>ID</label>: 1<br>
    <label>Book name</label>: Sample book<br>
    <label>Author email</label>: test@example.com<br>



    --===============1662479169==--

Template ``<app>/emails/<model><template_name_suffix>.html`` will be used if 
exists to render email content.

Templatetag ``render_fields`` can be used to influence which fields to render::

  {% load send_instance_tags %}
  {% render_fields object exclude="author_email,id" %}

