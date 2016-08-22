
# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import json
import time
from datetime import datetime

import tweepy
import requests

from creds import *
 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# would want a db in the future if I do more complex things
processed_files = []
 
fec_params = {
    'api_key': FEC_API_KEY,
    # don't want to flood the feed with repeats
    'min_receipt_date': datetime.now(),
}

while True:
    filings = requests.get('https://api.open.fec.gov/v1/efile/filings/?sort=-receipt_date&per_page=70', params=fec_params).json()

    if 'results' in filings:
        for record in filings['results']:
            if record['file_number'] not in processed_files:
                committee_name = str(record['committee_name'] or '')[:116]
                link = 'http://docquery.fec.gov/cgi-bin/forms/{0}/{1}'.format(record['committee_id'], record['file_number'])
                message = committee_name + ' ' + link
                if record['amends_file'] is not None:
                    message = committee_name[:106] + ' ' + link +' amendment'
                print (message)
                processed_files.append(record['file_number'])

                if len(processed_files) > 500:
                    processed_files = processed_files[50:] 
    
    time.sleep(10)
    