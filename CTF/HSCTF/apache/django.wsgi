import os
import sys

sys.path.append('/home/nullify/CTF/HSCTF')

os.environ['DJANGO_SETTINGS_MODULE'] = 'HSCTF.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()