import json
import logging
import os
import zipfile

import feedparser
import pandas as pd
import requests
import yaml

from datetime import datetime
from io import BytesIO

CONSUMER_KEY = os.environ.get("CONSUMER_KEY", None)
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", None)
NOW = datetime.now()
REQUEST_TIMEOUT = 10.0

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)


def add_article(url, tags=[]):
    global CONSUMER_KEY
    global ACCESS_TOKEN
    pocket_url = "https://getpocket.com/v3/add"
    tags.append("feed")
    data = {
        "consumer_key": CONSUMER_KEY,
        "access_token": ACCESS_TOKEN,
        "url": url,
        "tags": ",".join(tags),
    }
    ret = requests.post(pocket_url, data=data)
    if ret.text == "":
        logging.error("Pocket return empty string")
        return False
    ret = json.loads(ret.text)
    if ret.get("status", None) is None:
        logging.error("%s: %s", ret.get("error", ""), ret.get("message", ""))
        # exit()
        return False
    return ret["status"]


def get_last_time_rss_data(rss_url):
    global rss_database
    feed_location = rss_database["feed_url"] == rss_url
    idx = rss_database[feed_location].index.values[0]
    link_latest = rss_database.loc[idx, "saved_item_link_latest"]
    link_second_latest = rss_database.loc[idx, "saved_item_link_second_latest"]
    return idx, link_latest, link_second_latest


if os.path.exists("rss.yaml"):
    with open("rss.yaml", "r") as stream:
        try:
            rss_configs = yaml.safe_load(stream)
        except Exception as e:
            logging.error(f"Unexpected error when parsing yaml: {str(e)}")
            exit()
else:
    logging.error("rss.yaml not exists.")
    exit()

if os.path.exists("rss_database.zip"):
    rss_database = pd.read_csv("rss_database.zip")
else:
    rss_database = pd.DataFrame(
        columns=[
            "feed_url",
            "saved_item_link_latest",
            "saved_item_link_second_latest",
            "updated_time",
        ]
    )


# Iter all the feed configs
for rss_config in rss_configs:
    # Get the feed config
    rss_url = rss_config["url"]
    rss_tags = rss_config.get("tags", ["feed"])
    rss_filter = rss_config.get("filter", "")

    # Get the feed content
    logging.info(f"Checking {rss_url}")
    try:
        resp = requests.get(rss_url, timeout=REQUEST_TIMEOUT)
    except requests.ReadTimeout:
        logging.warning(f"Timeout when reading feed: {rss_url}")
        continue
    except requests.ConnectionError:
        logging.warning(f"Cannot access feed: {rss_url}")
        continue
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        continue
    content = BytesIO(resp.content)
    Feed = feedparser.parse(content)

    # Check the feed is first run or not
    flag_first_run = False
    if rss_url not in rss_database["feed_url"].values:
        rss_database.loc[-1] = {
            "feed_url": rss_url,
            "saved_item_link_latest": None,
            "saved_item_link_second_latest": None,
            "updated_time": None,
        }
        rss_database.index = rss_database.index + 1
        flag_first_run = True

    # Get last time rss data
    idx, link_latest, link_second_latest = get_last_time_rss_data(rss_url)

    # Sort the article according to the published time
    try:
        entries = Feed.get("entries", [])
        entries = sorted(entries, key=lambda e: e.published_parsed, reverse=True)
    except Exception as e:
        entries = Feed.get("entries", [])
        logging.error(f"Feed doesn't support published_parsed attribute: {rss_url}")

    # Iter the article in the feed
    for entry in entries:
        # Break if added
        if (entry.link == link_latest) or (entry.link == link_second_latest):
            break

        # Print article information
        entry_published_time = entry.get("published", None)
        logging.info(f"Article Info:\n\tTitle: {entry.title}\n\tPublished time: {entry_published_time}\n\tLink: {entry.link}")

        # Add the article
        if add_article(entry.link, rss_tags):
            logging.info("Article added")

            # Update the rss database
            if rss_database.loc[idx, "updated_time"] != NOW:
                rss_database.loc[idx, "saved_item_link_second_latest"] = link_latest
                rss_database.loc[idx, "saved_item_link_latest"] = entry.link
                rss_database.loc[idx, "updated_time"] = NOW
        else:
            logging.warning(f"Article not added: {entry.link}")

        # Add only one article when first run
        if flag_first_run:
            break


# Save the rss database
rss_database.sort_values("feed_url").to_csv("rss_database.csv", index=False)

# This is for CLI user
# As for GitHub Action user, the GitHub Action will compress the csv to zip
# file when running upload-artifact@v2
with zipfile.ZipFile("rss_database.zip", "w") as zf:
    zf.write("rss_database.csv")
