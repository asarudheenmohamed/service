"""Rating module celery tasks."""

import logging
import tempfile

import requests

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import FreshDesk
from app.rating.lib.rating_controller import RatingController
from config.celery import app
import json

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def create_fresh_desk_ticket(order_id):
    """Celery task to create fresh desk ticket."""

    controller = RatingController(order_id)

    controller.create_fresh_desk_ticket()


@app.task(name="app.rating.tasks.create_fresh_desk_attachment_ticket",
          base=TenderCutsTask)
def create_fresh_desk_attachment_ticket(data):
    """Celery task to create fresh desk attachment ticket.

    {u'data':
            u'{
                    "monitorUCID": "9049754955340984",
                    "UUI": "New_order_placement",
                    "Did": "914466949093",
                    "CampaignName": "Inbound_914466205652",
                    "Location": "Chennai",
                    "CallerID": "919080600507",
                    "PhoneName": "kannadasan",
                    "Skill": "New_order_placement",
                    "StartTime": "2018-08-06 16:59:33",
                    "EndTime": "2018-08-06 17:00:03",
                    "TimeToAnswer": "00:00:07",
                    "CallDuration": "00:00:30",
                    Duration": "00:00:23",
                    "FallBackRule": "AgentDial",
                    "DialedNumber": "9384842783",
                    "Type": "inbound",
                    "AgentID": "kannadasan_tendercuts",
                    "AgentPhoneNumber": "9384842783",
                    "AgentUniqueID": "68368",
                    "AgentName": "Kannadasan",
                    "Disposition": "Wrap up time exceeded :120",
                    "HangupBy": "UserHangup",
                    "Status": "Answered",
                    "AudioFile": "http://recordings.kookoo.in/tendercuts/tendercuts_9049754955340984_20180806165933.mp3",
                    "TransferType": "No Transfers",
                    "TransferredTo": "",
                    "Comments": "",
                    "DialStatus": "answered",
                    "Apikey": "KK78cb25cffffbcd44e5b6f1fcd554d0aa",
                    "AgentStatus": "answered",
                    "CustomerStatus": "answered",
                    "UserName": "tendercuts",
                    "CallerConfAudioFile": "", "ConfDuration": "00:00:00", "CampaignStatus": "ONLINE"}'}
    """
    data = json.loads(data['data'])

    logger.info(
        'CloudAgent: callback details:{} for the customer:{}'.format(
            data, data['CallerID']))

    type_ = {"inbound": "Call Inbound", "outbound": "Call outbound"}

    description = "The start:{} and end time:{} of the conversation will be attached into a ticket  (audio, agent name:{})".format(data[
        "StartTime"], data["EndTime"], data['AgentID'])

    audio_file = data['AudioFile']
    controller = FreshDesk()
    if not audio_file:
        controller.create_ticket_attachment(
            None,
            'CloudAgent:{} with {}'.format(
                data["Type"],
                data['CallerID']),
            description,
            data['CallerID'],
            type_.get(
                data["Type"]),
            data["AgentID"],
            data["Disposition"],
            data['Comments'])

        return

    doc = requests.get(audio_file)
    # create a temp mp3 file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3') as keyfile:
        with open(keyfile.name, 'wb') as fd:
            fd.write(doc.content)
            fd.close()
            logger.info(
                'CloudAgent: create attachment ticket for the customer:{}'.format(
                    data['CallerID']))
            controller.create_ticket_attachment(
                keyfile.name,
                'CloudAgent:{} with {}'.format(
                    data["Type"], data['CallerID']),
                description,
                data['CallerID'],
                type_.get(data["Type"]),
                data["AgentID"],
                data["Disposition"],
                data['Comments'])

        keyfile.close()
