import argparse
from bs4 import BeautifulSoup
import io
import json
import re
from requests import request
import sys

"""Iteration"""
VERSION = "1.2"


class NotRSSSource(Exception):
    """Resource on given URL does not contain RSS."""
    pass


class InvalidSourceURL(Exception):
    """Given URL is incorrect."""
    pass


class RequestError(Exception):
    """Error while request data from source."""
    pass


def validating_url(source):
    """Check that received source URL is not empty and starts with http."""
    if source and source != 'http://' and source != 'https://':
        if source.startswith('http://') or source.startswith('https://'):
            return True
        else:
            raise InvalidSourceURL(f"Invalid source URL '{source}'. Did you meant https://{source}")
    else:
        raise InvalidSourceURL(f"Source URL can't be empty.")


def get_data_from_source(source):
    return request("GET", source)


def get_tag_content(element, tag_name):
    """Return the text content of tag if it contain."""
    tag = element.find(tag_name)
    if tag:
        return tag.get_text()
    else:
        return None


def print_news(dump):
    """Print given news topics in stdout"""
    if not dump:
        return
    try:
        for source_url, source_dump in dump.items():
            print("\n{:#^100}".format(" " + source_url + " "))
            print("\n{:>12}: {}".format('Feed', source_dump['source_info']))
            for item_num, item in enumerate(source_dump['source_news'], 1):
                print()
                print("{:>12}| {}".format('Topic ' + str(item_num), item["title"] or "Topic has no title"))
                print("{:>12}| {}".format('Date', item["pubdate"] or "Topic has no publication date"))
                if item["links"]:
                    print("{:>12}| {}".format('Link', item["links"].pop(0)))
                if item["description"]:
                    print("{:>12}: {}".format('Description', item["description"]), "\n")
                if item["links"]:
                    print("{:>12}:".format("Links"))
                    for i, lnk in enumerate(item["links"], 1):
                        print("{:14} {}".format(i, lnk))
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
    response = get_data_from_source(source)
    print(f"Data was received successfully from '{source}'.")
    bs = BeautifulSoup(response.content, "xml")
    rss = bs.find('rss')
    if rss:
        rss_channel = rss.find("channel")
        resource_info = rss_channel.find("description").get_text() or rss_channel.find("title").get_text()
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
                raw_description = description = get_tag_content(item, "description")
                if raw_description:
                    description_links = re.findall(r"(http.*?)[>\s\"']", raw_description)
                    links.extend(lnk for lnk in description_links if lnk not in links)
                    description = BeautifulSoup(raw_description, 'lxml').get_text()

                item_content = {
                    "title": title,
                    "pubdate": pubdate,
                    "description": description,
                    "links": links
                }
                parsed_items_list.append(item_content)
        dump = {source: {'source_news': parsed_items_list, 'source_info': resource_info}}
        return dump
    else:
        raise NotRSSSource(f"Resource '{source}' has no RSS content")


def main():
    """Main function. Handle command-line arguments."""
    arg_parser = argparse.ArgumentParser(prog="rss_reader.py", description="Pure Python command-line RSS reader")
    arg_parser.add_argument('source', type=str, help="RSS URL",)
    arg_parser.add_argument('--version', action="version", help="Print version info", version=f"Version {VERSION}")
    arg_parser.add_argument('--json', action="store_true", help="Print result as JSON in stdout")
    arg_parser.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument('--limit', type=int, default=None, help="Limit news topics if this parameter provided")
    cli_arguments = arg_parser.parse_args()

    stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = stdout if cli_arguments.verbose else buffer
    try:
        news = parse_url(cli_arguments.source, limit=cli_arguments.limit)
    except Exception as e:
        sys.stdout = stdout
        print(e)
    else:
        sys.stdout = stdout
        if cli_arguments.json:
            print(json.dumps(news, ensure_ascii=False, indent=4))
        else:
            print_news(news)
