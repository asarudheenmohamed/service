"""Rating module celery tasks."""

import logging
import tempfile

import requests

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import FreshDesk
from app.rating.lib.rating_controller import RatingController
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def create_fresh_desk_ticket(order_id):
    """Celery task to create fresh desk ticket."""

    controller = RatingController(order_id)

    controller.create_fresh_desk_ticket()


@app.task(base=TenderCutsTask)
def create_fresh_desk_attachment_ticket(data):
    """Celery task to create fresh desk attachment ticket."""

    logger.info(
        'CloudAgent: callback details:{} for the customer:{}'.format(
            data, data['CallerID ']))
    controller = FreshDesk()
    audio_file = data['AudioFile']

    doc = requests.get(audio_file)

    # create a temp mp3 file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3') as keyfile:
        with open(keyfile.name, 'wb') as fd:
            fd.write(doc.content)
            fd.close()
            logger.info(
                'CloudAgent: create attachment ticket for the customer:{}'.format(
                    data['CallerID ']))

            controller.create_ticket_attachment(
                keyfile.name, 'CloudAgent:Inbunded Call with {}'.format(data['CallerID ']), data['Comments'], data['CallerID '])

        keyfile.close()
