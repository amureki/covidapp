import os


def get_wsgi_application():
    # Wrap with a function so that black rewrite of the code does not change
    # the import order.
    # We must first ensure environment variables and then import from
    # django-configurations.
    from configurations.wsgi import get_wsgi_application

    return get_wsgi_application()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Development")


application = get_wsgi_application()
