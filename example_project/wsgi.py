import os
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

from django.core.wsgi import get_wsgi_application
application = DjangoWhiteNoise(get_wsgi_application())
