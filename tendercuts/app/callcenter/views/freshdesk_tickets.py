from rest_framework import views, response
import dateutil.parser
import requests
import logging

logger = logging.getLogger()

REQUESTER_ID = {
    26000249534: 'Callcenter',
    26002435610: 'Client Support [Syrow]',
    26001678652: 'Liza'
}

STATUS = {
    0: 'Open',
    1: 'Pending',
    5: 'Resolved',
    3: 'Closed',
    4: 'Waiting for'
}


class FreshDeskTicketApi(views.APIView):

    def get(self, request):

        user_id = self.request.query_params['email']
        response = requests.get(
            "https://tendercuts.freshdesk.com/api/v2/tickets?email={}&per_page=20".format(user_id),
            auth=("UovHZV5Glhiw5YOHIP0Q", 'x'))

        data = response.json()
        for rec in data:
            # Remap agent names
            if rec['responder_id'] in REQUESTER_ID:
                rec['responder_id'] = REQUESTER_ID[rec['responder_id']]

            # Format date
            rec['created_at'] = format(
                dateutil.parser.parse(
                    rec['created_at']), "%d - %B")
            # Format status
            rec['status'] = STATUS.get(rec['status'], "Unknown")

            # construct url
            rec['url'] = "http://support.tendercuts.in/helpdesk/tickets/{}".format(rec[
                                                                                       'id'])
        return response.Response(data)
