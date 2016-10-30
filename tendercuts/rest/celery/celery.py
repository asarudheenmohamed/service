from celery import Celery

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tendercuts.settings")
django.setup()

app = Celery('tendercuts',
             broker='redis://localhost',
             backend='redis://localhost',
             include=['rest.celery.tasks'])

app.config_from_object('rest.celery.celeryconfig')

if __name__ == '__main__':
    app.start()