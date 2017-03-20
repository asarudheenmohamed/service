from .lib import ShadowFaxDriverController
from config.celery import app

@app.task
def push_orders_to_shawdowfax():
    controller = ShadowFaxDriverController()
    controller.push_orders()
