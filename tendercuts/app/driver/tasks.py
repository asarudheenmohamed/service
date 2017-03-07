from config.celery import app
from .lib import ShadowFaxDriverController

@app.task
def push_orders_to_shawdowfax():
    controller = ShadowFaxDriverController()
    controller.push_orders()
