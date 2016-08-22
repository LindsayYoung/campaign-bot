
# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import json
import os
import time
from datetime import datetime

import logging
import tweepy
import requests
 

auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])
api = tweepy.API(auth)

# would want a db in the future if I do more complex things
processed_files = []
 
fec_params = {
    'api_key': os.environ['FEC_API_KEY'],
    # don't want to flood the feed with repeats
    'min_receipt_date': datetime.now(),
}


logging.info('running')
api.update_status('deploy successful')

while True:
    filings = requests.get('https://api.open.fec.gov/v1/efile/filings/?sort=-receipt_date&per_page=70', params=fec_params).json()
    logging.info('True')
    if 'results' in filings:
        logging.info('looping')
        for record in filings['results']:
            if record['file_number'] not in processed_files:
                committee_name = str(record['committee_name'] or '')[:116]
                link = 'http://docquery.fec.gov/cgi-bin/forms/{0}/{1}'.format(record['committee_id'], record['file_number'])
                message = committee_name + ' ' + link
                if record['amends_file'] is not None:
                    message = committee_name[:106] + ' ' + link +' amendment'
                api.update_status(message)
                processed_files.append(record['file_number'])

                if len(processed_files) > 500:
                    processed_files = processed_files[50:] 
    
    time.sleep(10)
    