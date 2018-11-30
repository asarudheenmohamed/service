
# import requests
# import json

# api_key = "uoHER1yGfG9SAp7MXfb"
# domain = "support.tendercuts.in"
# password = "tendercuts1234"

# headers = {'Content-type': 'application/json'}


ticket = {
    'subject': 'Test Ticket',
    'description': 'Ticket detail',
    # 'email': 'asarudheen@tendercuts.in',
    'priority': 1,
    'status': 2,
    'phone': 8973111017,
    'name': 'asar',
    # 'name': 'sheik',
    # 'cc_emails': ['saravana@tendercuts.in'],
    "type": "Mail",
    "source": 2}


# # ('bat.jpg', open('bat.jpg', 'rb'), 'image/jpeg')

# multipart_data = [
#     # ('email', ('', 'asarudheen@tendercuts.in')),
#     # ('subject', ('', 'Ticket Title')),
#     # ('status', ('', "2")),
#     # ('priority', ('', "2")),
#     # ("type", ('', "Mail")),
#     # ('cc_emails[]', ('', 'saravana@tendercuts.in')),
#     # ('cc_emails[]', ('', 'asarudheenmohamed@gmail.com')),

#     ('attachments[]', ('aaja.jpg', open(
#         "/home/asarudheen/Downloads/mobile-banner-426x400.jpg", 'rb'))),
#     # ('description', ('', 'Ticket description.'))
# ]
# import pdb
# pdb.set_trace()
# # headers = {'Content-type': 'multipart/form-data'}
# r = requests.post(
#     "https://tendercuts.freshdesk.com/api/v2/tickets",
#     auth=(
#         api_key,
#         password),
#     headers=headers,
#     data=json.dumps(ticket),
#     files=multipart_data)
# import pdb
# pdb.set_trace()
# if r.status_code == 201:
#     print "Ticket created successfully, the response is given below" + r.content
#     print "Location Header : " + r.headers['Location']
# else:
#     print "Failed to create ticket, errors are displayed below,"
#     print r.content, 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPp'
#     response = json.loads(r.content)
#     print response["errors"]

#     print "x-request-id : " + r.headers['x-request-id']
#     print "Status Code : " + str(r.status_code)


import requests
import json

api_key = "uoHER1yGfG9SAp7MXfb"
domain = "tendercuts"
password = "x"

multipart_data = [

    ('attachments[]', (open(
        "/home/asarudheen/Documents/song.mp3"))),
]


import pdb
pdb.set_trace()
headers = {'Content-type': 'multipart/form-data'}
# headers = {'Content-type': 'application/json'}
# files = {
#     'attachments': open(
#         '/home/asarudheen/Downloads/Aaja_Nindiya.mp3',
#         'rb')}
r = requests.post(
    "https://" +
    domain +
    ".freshdesk.com/api/v2/tickets",
    auth=(
        api_key,
        password),
    files=multipart_data,
    # headers=headers,
    data=ticket)
import pdb
pdb.set_trace()
if r.status_code == 201:
    print "Ticket created successfully, the response is given below" + r.content
    print "Location Header : " + r.headers['Location']
else:
    print "Failed to create ticket, errors are displayed below,"
    print r.content, '[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    response = json.loads(r.content)
    print response, '[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[['
    # print response["errors"]

    print "x-request-id : " + r.headers['x-request-id']
    print "Status Code : " + str(r.status_code)


# test feshdesk attachment file creation

# from app.core.lib.communication import FreshDesk
# controller = FreshDesk()
# doc = requests.get(
# 'http://www.hrecos.org//images/Data/forweb/HRTVBSH.Metadata.pdf')
# with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf') as keyfile:
# with open(keyfile.name, 'wb') as fd:
# fd.write(doc.content)

#     controller.create_ticket_attachment(
#         keyfile.name, 'test', 'test ticket', 'asarudheen@tendercuts.in', 8973111017)
# keyfile.close()
