# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import json
import logging
import os

from datetime import datetime, timedelta
from time import strftime

import requests

import mail_script


tomorrow = datetime.today() + timedelta(1)
yesterday = datetime.today() - timedelta(1)
fec_params = {
    'api_key': os.environ['FEC_API_KEY'],
    'min_receipt_date': yesterday.strftime("%Y-%m-%d"),
    'max_receipt_date': tomorrow.strftime("%Y-%m-%d"),
    'page': 1,
}

base_url = 'https://api.open.fec.gov/v1/filings/?sort=-receipt_date&per_page=100'

def analize_file_num(num):
    if num is None:
        return ''
    if num and float(num) > 0:
        return num
    return ''

def analize_file(num, pdf):
    if num and float(num) > 0:
        return 'http://docquery.fec.gov/dcdev/posted/{0}.fec'.format(num)
    else:
        return pdf

def read_results(results, filing_dict):
    for r in results:
        result = {
            'sub_id': r['sub_id'], # primary key
            'document_description': r['document_description'],
            'committee_id': r['committee_id'],
            'committee_name': r['committee_name'],
            'file_number': r['file_number'],
            'amendment_indicator': r['amendment_indicator'],
            'report_type': r['report_type'],
            'report_type_full': r['report_type_full'],
            'total_receipts': r['total_receipts'],
            'total_disbursements': r['total_disbursements'],
            'total_independent_expenditures': r['total_independent_expenditures'],
            'receipt_date': r['receipt_date'],
            'coverage_start_date': r['coverage_start_date'],
            'coverage_end_date': r['coverage_end_date'],
            'pages': r['pages'],
            'fec_url': 'http://docquery.fec.gov/dcdev/posted/{0}.fec'.format(r['file_number']),
            'pdf_url': r['pdf_url'],
            'url': analize_file(r['file_number'], r['pdf_url']),
            'show_file_num': analize_file_num(r['file_number']),
        }
        if r['committee_id'] in filing_dict:
            filing_dict[r['committee_id']].append(result)
        else:
            filing_dict[r['committee_id']] = [result]

    return fec_params


def fetch_daily_files(total_pages, page):
    # replace with db
    filing_dict ={}
    while total_pages >= page:
        filings = requests.get(base_url, params=fec_params).json()
        if 'results' in filings:
            read_results(filings['results'], filing_dict)
            page = filings['pagination']['pages']
        else: break
    return filing_dict

def format_results(filing_dict):
    """fetch record by committee_id"""
    results = []
    for committee_id in filing_dict:
        info = {
            'committee_name': filing_dict[committee_id][0]['committee_name'] or '', 
            'committee_id': committee_id,
            'filings': filing_dict[committee_id]
        }
        results.append(info)

    return {
        'date': yesterday.strftime('%b %d, %Y'),
        'committees': results,
    }

def email_filings():
    filing_dict = fetch_daily_files(1, 1)
    template_data = format_results(filing_dict)
    server = mail_script.email_log_in()
    mail_script.mail_update(server, template_data, os.environ['ADMIN_EMAIL'])
