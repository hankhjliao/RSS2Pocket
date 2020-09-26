from datetime import datetime
from datetime import timedelta
from dateutil import parser
from io import BytesIO
import feedparser
import json
import logging
import os
import requests


update_interval = timedelta(hours=1)
CONSUMER_KEY = os.environ['CONSUMER_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO)
now = datetime.now()


def add_article(consumer_key, access_token, url):
    pocket_url = 'https://getpocket.com/v3/add'
    keys = {'consumer_key': consumer_key,
            'access_token': access_token,
            'url': url}
    get_json = requests.post(pocket_url, data = keys)
    get_json = json.loads(get_json.text)
    if get_json.get('status', None) is None:
        logging.error("%s: %s", get_json['error'], get_json['message'])
        exit()
    return get_json['status']


def time_parser(time_string):
    return parser.parse(time_string).replace(tzinfo=None)


with open('rss.txt') as f:
    rss_urls = f.readlines()

for rss_url in rss_urls:
    rss_url = rss_url.replace("\n", "")
    if rss_url.startswith("#") or (rss_url == ""): continue

    logging.info("Checking %s", rss_url)
    try:
        resp = requests.get(rss_url, timeout=10.0)
    except requests.ReadTimeout:
        logging.warning("Timeout when reading feed: %s", rss_url)
    except requests.ConnectionError:
        logging.warning("Cannot access feed: %s", rss_url)
    content = BytesIO(resp.content)
    Feed = feedparser.parse(content)

    feed_updated_time =  Feed.get('feed', {}).get('updated', None)
    logging.info("Feed last updated time: %s", feed_updated_time)

    if (feed_updated_time is None)\
            or ((now - time_parser(feed_updated_time)) <= update_interval):
        for entry in Feed.get('entries', []):
            entry_published_time =  entry.get('published', None)
            if (entry_published_time is None)\
                    or ((now - time_parser(entry_published_time)) <= update_interval):
                logging.info("Article Info:\n"\
                             "\tTitle: %s\n"\
                             "\tPublished time: %s\n"\
                             "\tLink: %s", entry.title, entry_published_time, entry.link)

                if add_article(CONSUMER_KEY, ACCESS_TOKEN, entry.link):
                    logging.info("Article added")
                else:
                    logging.warning("Article not added: %s", entry.link)

            else:
                break
    print()

