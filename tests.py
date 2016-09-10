""" super simple tests """
import os

import mail_script

import requests
from jinja2 import Template, Environment, FileSystemLoader

jinja_environment = Environment(autoescape=True,loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

test_filing = {
    'date': 'today',
    'committees': [
        {
            'committee_name': 'test committee', 
            'committee_id': '123',
            'committee_name': 'Lindsay\'s fictional committee',
            'filings': [
                {
                    'file_number': '123456',
                    'amendment_indicator': 'N',
                    'report_type': 'F3',
                    'report_type_full': 'Sept Quarterly',
                    'total_receipts': '1000',
                    'total_disbursements': '5000',
                    'total_independent_expenditures': '23',
                    'receipt_date': '08/30/2016',
                    'coverage_start_date': '07/01/2016',
                    'coverage_end_date': '08/30/2016',
                    'url': 'www.example.com',
                },
                {
                    'candidate_name': 'person',
                    'file_number': '12346',
                    'amendment_indicator': 'N',
                    'report_type': 'F3',
                    'report_type_full': 'Sept Quarterly',
                    'total_receipts': '1000',
                    'total_disbursements': '5000',
                    'total_independent_expenditures': '23',
                    'receipt_date': '08/30/2016',
                    'coverage_start_date': '07/01/2016',
                    'coverage_end_date': '08/30/2016',
                    'url': 'www.example.com',
                },
            ]
        }
    ]
}

def test_email_render():
    template = jinja_environment.get_template('test_template.html')
    text = template.render(test_filing)
    print(text)

def test_email(data):
    server = mail_script.email_log_in()
    mail_script.mail_update(server, data, os.environ['ADMIN_EMAIL'])
    
test_email_render()
test_email(test_filing)


# data =        (r['sub_id'], # primary key
#         r['committee_id'],
#         r['committee_name'],
#         r['candidate_name']
#         r['file_number'],
#         r['amendment_indicator'],
#         r['report_type']
#         r['report_type_full'],
#         r['total_receipts'],
#         r['total_disbursements'],
#         r['total_independent_expenditures'],
#         r['receipt_date'],
#         r['coverage_start_date'],
#         r['coverage_end_date'],
#         r['pages'],
#         'http://docquery.fec.gov/dcdev/posted/{0}.fec'.format(r['file_number'])