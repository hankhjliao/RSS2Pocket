from datetime import datetime
from datetime import timedelta
from dateutil import parser
from io import BytesIO
import feedparser
import json
import logging
import os
import requests
import time


update_interval = timedelta(hours=1, minutes=5)
CONSUMER_KEY = os.environ['CONSUMER_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO)
now = datetime.now()


def add_article(consumer_key, access_token, url):
    pocket_url = 'https://getpocket.com/v3/add'
    keys = {'consumer_key': consumer_key,
            'access_token': access_token,
            'url': url,
            'tags': 'feed',
           }
    get_json = requests.post(pocket_url, data = keys)
    get_json = json.loads(get_json.text)
    if get_json.get('status', None) is None:
        logging.error("%s: %s", get_json['error'], get_json['message'])
        exit()
    return get_json['status']


def timestamp_to_datetime(time_string):
    return datetime.fromtimestamp(time.mktime(time_string))


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
        print()
        continue
    except requests.ConnectionError:
        logging.warning("Cannot access feed: %s", rss_url)
        print()
        continue
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
        print()
        continue
    content = BytesIO(resp.content)
    Feed = feedparser.parse(content)

    feed_updated_time = Feed.get('feed', {}).get('updated', None)
    feed_updated_time_parsed = Feed.get('feed', {}).get('updated_parsed', None)
    logging.info("Feed last updated time: %s", feed_updated_time)

    if (feed_updated_time is None) or ((now - timestamp_to_datetime(feed_updated_time_parsed)) <= update_interval):
        for entry in Feed.get('entries', []):
            entry_published_time =  entry.get('published', None)
            entry_published_time_parsed = entry.get('published_parsed', None)
            if (entry_published_time is None) or ((now - timestamp_to_datetime(entry_published_time_parsed)) <= update_interval):
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

