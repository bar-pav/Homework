import argparse
from bs4 import BeautifulSoup
import io
import json
import re
from requests import request
from requests.exceptions import HTTPError
import sys

"""Iteration"""
VERSION = "1.1"

ap = argparse.ArgumentParser(prog="rss_reader.py", description="Pure Python command-line RSS reader")
ap.add_argument('source', type=str, help="RSS URL")
ap.add_argument('--version', action="version", help="Print version info", version=f"Version {VERSION}")
ap.add_argument('--json', action="store_true", help="Print result as JSON in stdout")
ap.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
ap.add_argument('--limit', type=int, default=None, help="Limit news topics if this parameter provided")
ap_namespace = ap.parse_args()


class NotRSSSource(Exception):
    """Resource on given URL does not contain RSS."""
    pass


class InvalidSourceURL(Exception):
    """Given URL is incorrect."""
    pass


def validating_url(source):
    """Check that received source URL is not empty and starts with http."""
    if source:
        if source.startswith('http://') or source.startswith('https://'):
            return True
        else:
            raise InvalidSourceURL(f"Invalid source URL '{source}'. It must starts with http:// or https://")
    else:
        raise InvalidSourceURL(f"Source URL can't be empty.")


def get_tag_content(element, tag_name):
    """Return tag text content if it contain."""
    tag = element.find(tag_name)
    if tag:
        return tag.get_text()
    else:
        return None


def print_news(dump):
    """Print given news topics in stdout"""
    if not dump:
        print("Empty object")
        return
    try:
        print("Feed:", dump["feed"], '\n')
        for item_num, item in enumerate(dump["news"], 1):
            print(f"{item_num:4} " + '-' * 80, "\n")
            print("Title:", item["title"] or "Topic has no title")
            print("Date:", item["date"] or "Topic has no publication date")
            print("Link:", item["link"] or "Topic has no link")
            if item["description"]:
                print()
                print("Description:", item["description"])
                print()
            if item["links"]:
                print("Links:")
            for i, lnk in enumerate(item["links"], 1):
                print(i, lnk)
            print()
    except KeyError as k:
        print(f"Object has incorrect structure for printing: {k}.")


def parse_url(source, limit=None):
    """Retrieves news topics from the given URL.

    Attributes:
        - source -- URL address of RSS resource.
        - limit -- The number of news topics which will be returned. If not specified,
                   will return all available feed.
    """
    validating_url(source)
    print(f"Receiving data from '{source}' ...")
    response = None
    try:
        response = request("GET", source)
        response.raise_for_status()
    except HTTPError as he:
        print(f"HTTP error occurred while receiving data from '{source}': {he}.")
    except Exception as exc:
        print(f"Exception occurred while receiving data from '{source}': {exc}.")
        raise
    else:
        print(f"Data was received successfully from '{source}'.")
    bs = BeautifulSoup(response.content, "xml")
    rss = bs.find('rss')   # Check if the resource contains rss
    if rss:
        rss_channel = rss.find("channel")
        resource_info = rss_channel.find("description").get_text()
        items = rss_channel.findAll('item')
        parsed_items_list = []
        if items:
            print("Resource has {} news topics. {}".format(len(items),
                                                           f"Display limit: {limit}" if limit else ""), '\n')
            if limit is not None and limit >= 0:
                items = items[:limit]
            for item in items:
                title = get_tag_content(item, "title")
                pubdate = get_tag_content(item, 'pubDate')
                link = item.find("link")
                link = link.get_text() if link else ""
                links = [link] if link else []
                for tag in item.find_all(True):
                    lnk = tag.get("url", None) or tag.get("href", None) or tag.get("src", None)
                    if lnk and lnk not in links:
                        links.append(lnk)
                description = get_tag_content(item, "description")
                if description:
                    description_links = re.findall(r"(http.*?)[>\s\"']", description)
                    links.extend(lnk for lnk in description_links if lnk not in links)
                    description = BeautifulSoup(description, "lxml")
                    description_tags = description.find_all(True)
                    if description_tags:
                        description = description.get_text()

                item_content = {
                    "title": title,
                    "date": pubdate,
                    "link": link,
                    "description": description,
                    "links": links,
                }
                parsed_items_list.append(item_content)
        dump = {"feed": resource_info, "news": parsed_items_list}
        return dump
    else:
        raise NotRSSSource(f"Resource '{source}' has no RSS content")


if __name__ == "__main__":
    stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = stdout if ap_namespace.verbose else buffer
    try:
        news = parse_url(ap_namespace.source, limit=ap_namespace.limit)
    except Exception as e:
        print(e)
    else:
        sys.stdout = stdout
        if ap_namespace.json:
            print(json.dumps(news, ensure_ascii=False, indent=4))
        else:
            print_news(news)
