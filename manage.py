import logging
from sys import argv

import bot
import file_updates

job = argv[1]

def start_tweet_bot():
    """tweet
    Runs the @young_bots twitter"""
    logging.info('Running tweet bot...')
    bot.tweet_filings()

def email_updates():
    """email
    Emails filings in the morning"""
    logging.info('Starting emails')
    file_updates.email_filings()
    logging.info('Emails complete')

if __name__ == "__main__":
    if job == 'tweet':
        start_tweet_bot()
    if job == 'email':
        email_updates()