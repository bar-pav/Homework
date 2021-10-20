import argparse
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from dateutil import utils
import io
import json
import os
import re
from requests import request
import sqlite3
import sys


"""Iteration"""
VERSION = "1.3"
db_path = "cached_news.db"


class NotRSSSource(Exception):
    """Resource on given URL does not contain RSS."""
    pass


class InvalidSourceURL(Exception):
    """Given URL is incorrect."""
    pass


class RequestError(Exception):
    """Error while request data from source."""
    pass


class NoNewsForDate(Exception):
    """Error if no news for the date in cache"""
    pass


class RSSReader:
    """RSSReader class.  Creates an object that includes a list of news items retrieved from source URL.
       and methods for presenting them based on command line arguments passed during creating of instance.
    """
    def __init__(self, cli_arguments):
        self.arg_url = cli_arguments.source
        self.arg_limit = cli_arguments.limit
        self.arg_date = cli_arguments.date
        if self.arg_date:
            self.news = self.fetch_news_from_cache()
        else:
            self.validating_url()
            self.response = self.get_data_from_source()
            self.news = self.parse_response()
            self.cache_news()

    def validating_url(self):
        """Check that received source URL is not empty and starts with http."""
        if self.arg_url and self.arg_url != 'http://' and self.arg_url != 'https://':
            if self.arg_url.startswith('http://') or self.arg_url.startswith('https://'):
                return True
            else:
                raise InvalidSourceURL(f"Invalid source URL '{self.arg_url}'. Did you meant https://{self.arg_url}")
        else:
            raise InvalidSourceURL(f"Source URL can't be empty.")

    def get_data_from_source(self):
        """Sends a request and return response object"""
        print(f"Receiving data from '{self.arg_url}' ...")
        try:
            response = request("GET", self.arg_url)
        except Exception:
            raise RequestError(f"Error occurred while receiving data from '{self.arg_url}'.")
        else:
            print(f"Data was received successfully from '{self.arg_url}'.")
            return response

    @classmethod
    def get_tag_content(cls, element, tag_name):
        """Return the text content of tag if it contain."""
        tag = element.find(tag_name)
        if tag:
            return tag.get_text()
        else:
            return None

    def parse_response(self):
        """Retrieves news topics from the self.response."""
        bs = BeautifulSoup(self.response.content, "xml")
        rss = bs.find('rss')
        if rss:
            rss_channel = rss.find("channel")
            resource_info = rss_channel.find("description").get_text() or rss_channel.find("title").get_text()
            items = rss_channel.findAll('item')
            parsed_items_list = []
            if items:
                print("Resource has {} news topics. {}".
                      format(len(items), f"Display limit: {self.arg_limit}" if self.arg_limit else ""), '\n')
                if self.arg_limit is not None and self.arg_limit >= 0:
                    items = items[:self.arg_limit]
                for item in items:
                    title = self.get_tag_content(item, "title")
                    pubdate = self.get_tag_content(item, 'pubDate')
                    link = item.find("link")
                    link = link.get_text() if link else ""
                    links = [link] if link else []
                    for tag in item.find_all(True):
                        lnk = tag.get("url", None) or tag.get("href", None) or tag.get("src", None)
                        if lnk and lnk not in links:
                            links.append(lnk)
                    raw_description = self.get_tag_content(item, "description")
                    if raw_description:
                        description_links = re.findall(r"(http.*?)[>\s\"']", raw_description)
                        links.extend(lnk for lnk in description_links if lnk not in links)
                        raw_description = BeautifulSoup(raw_description, 'lxml').get_text()

                    item_content = {
                        "title": title,
                        "pubdate": pubdate,
                        "description": raw_description,
                        "links": links
                    }
                    parsed_items_list.append(item_content)
            dump = {self.arg_url: {'source_news': parsed_items_list, 'source_info': resource_info}}
            return dump
        else:
            raise NotRSSSource(f"Resource '{self.arg_url}' has no RSS content")

    def print_news(self):
        """Print given news topics in stdout"""
        if not self.news:
            return
        try:
            for source_url, source_dump in self.news.items():
                print("\n{:#^100}".format(" " + source_url + " "))
                print("\n{:>12}: {}".format('Feed', source_dump['source_info']))
                for item_num, item in enumerate(source_dump['source_news'], 1):
                    print()
                    print("{:>12}| {}".format('Topic ' + str(item_num), item["title"] or "Topic has no title"))
                    print("{:>12}| {}".format('Date', item["pubdate"] or "Topic has no publication date"))
                    print("{:>12}| {}".format('Link', item["links"].pop(0) or "Topic has no link"))
                    if item["description"]:
                        print("{:>12}: {}".format('Description', item["description"]))
                    if item["links"]:
                        print("{:>12}:".format("Links"))
                        for i, lnk in enumerate(item["links"], 1):
                            print("{:14} {}".format(i, lnk))
        except KeyError as k:
            print(f"Object has incorrect structure for printing: {k}.")

    def print_json(self):
        """Prints news in json format in stdout."""
        print(json.dumps(self.news, ensure_ascii=False, indent=4))

    def cache_news(self):
        """Stores news in local SQLite3 database."""
        print("Caching news in the DB")
        print("\tConnecting to the DB ...")
        if os.path.exists(db_path):
            db_exist = True
        else:
            db_exist = False
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        print("\tConnection OK.")
        if not db_exist:
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS source (
                                id integer PRIMARY KEY,
                                source_url text,
                                source_info text,
                                CONSTRAINT unique_source UNIQUE (source_url, source_info)
                                );""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS news (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                date varchar(255),
                                source_id integer,
                                item_json text,
                                CONSTRAINT unique_news UNIQUE (item_json),
                                FOREIGN KEY (source_id) REFERENCES source(id)
                                );""")
        print("\t\tCaching news\n\t\t...")
        for source, source_dump in self.news.items():
            source_exist = cursor.execute("""SELECT * FROM source WHERE source_url=(?)""", (source,)).fetchone()
            if source_exist:
                source_id = source_exist[0]
            else:
                added = cursor.execute("""INSERT INTO source (source_url, source_info) VALUES (?, ?)""",
                                       (source, source_dump.get('source_info')))
                source_id = added.lastrowid
            connection.commit()
            for item in source_dump['source_news'][::-1]:
                date = date_parser.parse(item["pubdate"]) if item["pubdate"] else utils.today()
                cursor.execute("""INSERT OR IGNORE INTO news (date, source_id, item_json)
                                    VALUES (?, ?, ?)""", (date.strftime("%Y%m%d"),
                                                          source_id,
                                                          json.dumps(item, ensure_ascii=False)))
        connection.commit()
        print("\t\tNews saved in local DB.")
        print("\tClosing connection to DB...")
        connection.close()
        print("\tConnection closed.")

    def fetch_news_from_cache(self):
        """Retrieves news from local database for the date."""
        if os.path.exists(db_path):
            print(f"Fetching news from the DB")
            print("\tConnecting to DB ...")
            connection = sqlite3.connect(db_path)
            print("\tConnection OK.")
            print(f"\t\tFetching news for the date '{self.arg_date}'" +
                  (f" for source '{self.arg_url}'" if self.arg_url else ""), "\n\t\t...")
            cursor = connection.cursor()
            dump = {}
            select_query = (f"""SELECT {'source.source_url,' if not self.arg_url else ''} news.item_json 
                            FROM news JOIN source ON news.source_id = source.id WHERE news.date=(?) 
                            {'and source.source_url=(?)' if self.arg_url else ''} ORDER BY news.id DESC""",
                            (self.arg_date, self.arg_url) if self.arg_url else (self.arg_date,))
            select_result = cursor.execute(*select_query).fetchall()[:self.arg_limit]
            print(f"\t\tFetched {len(select_result)} news from local DB.")
            if not select_result:
                raise NoNewsForDate(f"No news for the date '{self.arg_date}' in cache.")
            if self.arg_url:
                dump[self.arg_url] = []
                for item in select_result:
                    dump[self.arg_url].append(json.loads(item[0]))
            else:
                for item in select_result:
                    dump[item[0]] = dump.get(item[0], [])
                    dump[item[0]].append(json.loads(item[1]))
            for source in dump.keys():
                news = dump[source]
                dump[source] = {}
                dump[source]['source_news'] = news   # [::-1]
                dump[source]['source_info'] = cursor.execute("""SELECT source_info FROM source WHERE source_url=(?)""",
                                                             (source,)).fetchone()[0]
            print("\tClosing connection to DB...")
            connection.close()
            print("\tConnection closed.")
            return dump
        else:
            raise NoNewsForDate("No cached news yet.")


def parse_cli_arguments():
    """Creates ArgumentParser instance and add command line attributes to it."""
    arg_parser = argparse.ArgumentParser(prog="rss_reader.py", description="Pure Python command-line RSS reader")
    arg_parser.add_argument('source', type=str, nargs='?', default="", help="RSS URL",)
    arg_parser.add_argument('--version', action="version", help="Print version info", version=f"Version {VERSION}")
    arg_parser.add_argument('--json', action="store_true", help="Print result as JSON in stdout")
    arg_parser.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument('--limit', type=int, default=None, help="Limit news topics if this parameter provided")
    arg_parser.add_argument('--date', type=str, default=None, help="Retrieves news for the date, %Y%m%d")
    return arg_parser


def main():
    """Main function. Handle command-line arguments."""
    arg_parse = parse_cli_arguments()
    if len(sys.argv) == 1:
        arg_parse.print_usage()
        return
    cli_arguments = arg_parse.parse_args()
    stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = stdout if cli_arguments.verbose else buffer
    try:
        reader = RSSReader(cli_arguments)
    except Exception as e:
        sys.stdout = stdout
        print(e)
    else:
        sys.stdout = stdout
        if cli_arguments.json:
            reader.print_json()
        else:
            reader.print_news()


if __name__ == "__main__":
    main()
