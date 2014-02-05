import os
import sys

sys.path.append('/etc/wwwmain')
os.environ['DJANGO_SETTINGS_MODULE'] = 'webvelogui.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
