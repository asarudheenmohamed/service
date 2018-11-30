import hashlib
import requests
import pandas as pd
import dateutil.parser
from datetime import timedelta

COMMAND = "get_Transaction_Details"
wsUrl = "{}merchant/postservice?form=2".format('https://info.payu.in/')
secret = 'xV0BSL'
date_from = (
    dateutil.parser.parse('2018-05-03') + timedelta(days=-1)).date(),
date_to = (
    dateutil.parser.parse('2018-05-03') + timedelta(days=1)).date(),
print(date_from, date_to)
# date_from = "2018-05-03",
# date_to = "2018-05-03",
merchant_id = 'U6KiaG3M'

val = ("{}|{}|{}|{}".format(secret, COMMAND, date_from[0], merchant_id))
hash_val = hashlib.sha512(val.encode('utf-8'))
data = {
    'key': secret,
    'hash': hash_val.hexdigest(),
    'var1': date_from,
    'var2': date_to,
    'command': COMMAND}

res = requests.post(wsUrl, data=data, timeout=30)

response = res.json()
payu_df = pd.DataFrame(response['Transaction_details'])
filtered_payu_df = payu_df[payu_df['status'] == 'captured']
print(filtered_payu_df)
