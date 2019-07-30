=====
HERMES
=====

HERMES is a Sendgrid middleware to send emails

Quick start
-----------
0. Install with PIP
    pip install git+https://comuna18_ricardo@bitbucket.org/comuna18/hermes.git

1. Add "hermes" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'hermes',
    ]

2. Include the settings config variables::

    SENDGRID_API_KEY = 'SA.KEY'
    SENDGRID_DEFAULT_SENDER = 'email@example.com'
    BCC_RECIPIENTS_LIST = ['otheremail@example.com']

3. Run `python manage.py migrate` to create hermes models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to check emails logs (you'll need the Admin app enabled).

