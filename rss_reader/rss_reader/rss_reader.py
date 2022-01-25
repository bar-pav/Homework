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
from contextlib import redirect_stderr
from xhtml2pdf import pisa

"""Iteration"""
VERSION = "1.5"

db_path = "cached_news.db"
html_result_file = "news.html"
pdf_result_file = "news.pdf"


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
       and methods for presenting them based on command line arguments passed when creating of instance.
    """
    def __init__(self, cli_arguments, colored):
        self._arg_url = cli_arguments.source
        self._arg_limit = cli_arguments.limit
        self._arg_date = cli_arguments.date
        self._arg_to_html = cli_arguments.to_html
        self._arg_to_pdf = cli_arguments.to_pdf
        self._colored = colored
        if colored:
            self.print_success = colored.print_success
            self.print_info = colored.print_info
            self.print_exception = colored.print_exceptions
        else:
            self.print_success = print
            self.print_info = print
            self.print_exception = print
        self._html_template = None
        if self._arg_date:
            self.news = self.fetch_news_from_cache()
        else:
            self.validating_url()
            self.response = self.get_data_from_source()
            self.news = self.parse_response()
            self.cache_news()

    def validating_url(self):
        """Check that received source URL is not empty and starts with http."""

        if self._arg_url and self._arg_url != 'http://' and self._arg_url != 'https://':
            if self._arg_url.startswith('http://') or self._arg_url.startswith('https://'):
                return True
            else:
                raise InvalidSourceURL(f"Invalid source URL '{self._arg_url}'")
        else:
            raise InvalidSourceURL(f"Source URL can't be empty.")

    def get_data_from_source(self):
        """Sends a request and return response object"""
        self.print_info(f"Receiving data from '{self._arg_url}' ...")
        try:
            response = request("GET", self._arg_url, headers={'User-agent': 'Mozilla/5.0'}, timeout=10)
        except Exception:
            raise RequestError(f"Error occurred while receiving data from '{self._arg_url}'.")
        else:
            self.print_success(f"Data was received successfully from '{self._arg_url}'.")
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
        """Retrieves news topics from the response of request.

        """
        bs = BeautifulSoup(self.response.content, "xml")
        rss = bs.find('rss')
        if rss:
            rss_channel = rss.find("channel")
            rss_channel_title = rss_channel.find("title").get_text()
            rss_channel_description = rss_channel.find("description").get_text()
            resource_info = ". ".join([rss_channel_title, (rss_channel_description if
                                                           rss_channel_description != rss_channel_title else "")])
            items = rss_channel.findAll('item')
            parsed_items_list = []
            if items:
                self.print_success("Resource has {} news topics. {}".
                                   format(len(items), f"Display limit: {self._arg_limit}" if self._arg_limit else "") +
                                   '\n')
                if self._arg_limit is not None and self._arg_limit >= 0:
                    items = items[:self._arg_limit]
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
                        # raw_description = BeautifulSoup(raw_description, 'lxml').get_text()

                    item_content = {
                        "title": title,
                        "pubdate": pubdate,
                        "description": raw_description,
                        "links": links
                    }
                    parsed_items_list.append(item_content)
            dump = {self._arg_url: {'source_news': parsed_items_list,
                                    'source_info': resource_info,
                                    }
                    }
            return dump
        else:
            raise NotRSSSource(f"Resource '{self._arg_url}' has no RSS content")

    def print_news(self):
        """Print given news topics in stdout"""
        import table
        if not self.news:
            return
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        row_names = ['Topic ', 'Date', 'Link', 'Description', 'Links']
        table.get_max_column_width(row_names)
        table.colored = self._colored
        try:
            for source_url, source_dump in self.news.items():
                table.print_header(re.findall(r'//([A-Za-z0-9./]*)', source_url)[0])
                table.print_row('Feed', source_dump['source_info'])
                table.print_horizontal_border()
                for item_num, item in enumerate(source_dump['source_news'], 1):
                    table.print_row('Topic ' + str(item_num), item["title"] or "Topic has no title")
                    table.print_horizontal_row_separator()
                    table.print_row('Date', item["pubdate"] or "Topic has no publication date")
                    table.print_horizontal_row_separator()
                    if item["links"]:
                        table.print_row('Link', item["links"].pop(0) or "Topic has no link")
                    table.print_horizontal_row_separator()
                    if item["description"]:
                        table.print_row('Description', BeautifulSoup(item["description"], 'lxml').get_text())
                        # print('Description', BeautifulSoup(item["description"], 'lxml').get_text())
                    table.print_horizontal_row_separator()
                    if item["links"]:
                        table.print_row('Links', '\n'.join(f"{i}. {lnk}" for i, lnk in enumerate(item["links"], 1)))
                    table.print_horizontal_border()
        except KeyError as k:
            self.print_exception(f"Object has incorrect structure for printing: {k}.")

    def print_json(self):
        """Prints news in json format in stdout."""
        for source in self.news.keys():
            for item in self.news[source]["source_news"]:
                if item["description"]:
                    item["description"] = BeautifulSoup(item["description"], 'lxml').get_text()
                else:
                    continue
        print(json.dumps(self.news, ensure_ascii=False, indent=4))

    def cache_news(self):
        """Stores news in local SQLite3 database."""
        self.print_info("Caching news in the DB")
        self.print_info("\tConnecting to the DB ...")
        if os.path.exists(db_path):
            db_exist = True
        else:
            db_exist = False
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        self.print_success("\tConnection OK.")
        if not db_exist:
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS source (
                                id integer PRIMARY KEY,
                                source_url text,
                                source_info text,
                                CONSTRAINT unique_source UNIQUE (source_url, source_info)
                                );""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS news (
                                id integer PRIMARY KEY,
                                date varchar(255),
                                source_id integer,
                                item_json text,
                                CONSTRAINT unique_news UNIQUE (item_json),
                                FOREIGN KEY (source_id) REFERENCES source(id)
                                );""")
        self.print_info("\t\tCaching news\n\t\t...")

        next_id = cursor.execute("""SELECT id FROM news ORDER BY id DESC LIMIT 1""").fetchone()
        if next_id:
            next_id = next_id[0] + 1
        else:
            next_id = 1
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
                added_id = cursor.execute("""INSERT OR IGNORE INTO news (id, date, source_id, item_json)
                                    VALUES (?, ?, ?, ?)""", (next_id, date.strftime("%Y%m%d"),
                                                             source_id,
                                                             json.dumps(item, ensure_ascii=False)))
                next_id = (added_id.lastrowid + 1) if added_id else next_id
        connection.commit()
        self.print_success("\t\tNews saved in local DB.")
        self.print_info("\tClosing connection to DB...")
        connection.close()
        self.print_info("\tConnection closed.")

    def fetch_news_from_cache(self):
        """Retrieves news from local database for the date."""
        if os.path.exists(db_path):
            self.print_info(f"Fetching news from the DB")
            self.print_info("\tConnecting to DB ...")
            connection = sqlite3.connect(db_path)
            self.print_success("\tConnection OK.")
            self.print_info(f"\t\tFetching news for the date '{self._arg_date}'" +
                            (f" for source '{self._arg_url}'" if self._arg_url else ""), "\n\t\t...")
            cursor = connection.cursor()
            dump = {}
            select_query = (f"""SELECT {'source.source_url,' if not self._arg_url else ''} news.item_json 
                            FROM news JOIN source ON news.source_id = source.id WHERE news.date=(?) 
                            {'and source.source_url=(?)' if self._arg_url else ''} ORDER BY news.id DESC""",
                            (self._arg_date, self._arg_url) if self._arg_url else (self._arg_date,))
            select_result = cursor.execute(*select_query).fetchall()[:self._arg_limit]
            self.print_success(f"\t\tFetched {len(select_result)} news from local DB.")
            if not select_result:
                raise NoNewsForDate(f"No news for the date '{self._arg_date}' in cache.")
            if self._arg_url:
                dump[self._arg_url] = []
                for item in select_result:
                    dump[self._arg_url].append(json.loads(item[0]))
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
            self.print_info("\tClosing connection to DB...")
            connection.close()
            self.print_info("\tConnection closed.")
            return dump
        else:
            raise NoNewsForDate("No cached news yet.")

    def convert2html(self, to_file=True):
        """Save news as html file."""
        def create_html_links(links):
            """Creates a <ul> tag with a list of passed links"""
            if links:
                links_list = []
                for link in links:
                    links_list.append(f"<a href={link}>{link if len(link) < 50 else link[:50] + '...'}</a>")
                return f"""<ul>Links:<li>
                            {'</li><li>'.join(link for link in links_list)}
                        </li>
                    </ul>"""

        def create_html_item(item):
            """Creates block for one news"""
            return f"""\n<div class="item">
                             <div class="title"><h3>{item["title"] or ""}</h3></div>
                             <div class="item_content">
                                 <div class="pubdate"><h6>{item["pubdate"] or ""}</h6></div>
                                 <div class="description">{item["description"] or ""}</div>
                                 <div class="links"> {create_html_links(item["links"])} </div>
                             </div>
                         </div>"""

        font_path_windows = "C:\\Windows\\Fonts\\Calibri.ttf"
        font_path_linux = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        font_path_linux_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
        font_path_linux_italic = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Oblique.ttf"

        def create_style_tag(with_borders=True):
            """Returns a style tag with a different border decoration of the item tag,
                depending on the format of saving the document"""
            return f"""<style>
                            @font-face {{ font-family: DejaVuSans; 
                                          src: url({font_path_windows if sys.platform == 'win32' else font_path_linux});}}
                            @font-face {{ font-family: DejaVuSans; 
                                          src: url({font_path_windows if sys.platform == 'win32' else font_path_linux_bold}); 
                                          font-weight: bold; }}
                            @font-face {{ font-family: DejaVuSans; 
                                          src: url({font_path_windows if sys.platform == 'win32' else font_path_linux_italic}); 
                                          font-style: italic; }}
                            .source_info {{ font-size: 2em; 
                                            margin-top: 1.2em;
                                            margin-bottom: 1.2em;
                                            width: 80%;
                                            margin-left: auto;
                                            margin-right: auto; 
                                            }}
                            .item {{ display: block;
                                     margin: 5px;
                                     padding: 10px;
                                     width: 50%;
                                     margin-left: auto;
                                     margin-right: auto;
                                     {"border: 2px solid #e4e1e1; border-radius: 10px;" if with_borders else ""}
                              }}
                            .title {{ font-weight: bold; }}
                            .item_content {{ margin-left: 25px; margin-bottom: 0px; padding: 0px; }}
                            .pubdate {{ font-size: 0.6; margin-top: 0px; padding: 0px; }}
                            .description img {{ width: 100%; }}
                            .links {{ width: 100%; }}
                            html {{ font-family: "DejaVuSans"; }}
                            h3 {{ margin: 0px; padding: 5px; }}
                            h6 {{ margin-top: 0px; padding: 0px; }}   
                        </style>"""
        if not self._html_template:
            all_sources = []
            for source in self.news.keys():
                one_source_news_html = f"""<div class="channel">
                                                <div class="source_info">{self.news[source]["source_info"]}</div>
                                                    {"".join(create_html_item(item) 
                                                             for item in self.news[source]["source_news"])}
                                           </div>"""
                all_sources.append(one_source_news_html)
            html_template = f"""<!DOCTYPE html>
                                <html>
                                   <head>
                                        <meta charset=utf-8">
                                        {{style_tag}}
                                      <title>RSS Reader</title>
                                   </head>
                                   <body>
                                   {''.join(source for source in all_sources)}
                                   </body>
                                </html>"""
            self._html_template = html_template
        if to_file:
            with open(html_result_file, 'w') as f:
                f.write(self._html_template.format(style_tag=create_style_tag(True)))
        else:
            return self._html_template.format(style_tag=create_style_tag(False))

    def convert2pdf(self):
        """Convert HTML template to PDF"""
        with redirect_stderr(None):
            result_file = open(pdf_result_file, "w+b")
            pisa.CreatePDF(
                self.convert2html(False),
                dest=result_file, encoding='utf-8')
            result_file.close()


def parse_cli_arguments():
    """Creates ArgumentParser instance and add attributes to it."""
    arg_parser = argparse.ArgumentParser(prog="rss_reader.py", description="Pure Python command-line RSS reader")
    arg_parser.add_argument('source', type=str, nargs='?', help="Input RSS URL. Must start with 'http[s]://'")
    arg_parser.add_argument('--version', action="version", help="Print version info", version=f"Version {VERSION}")
    arg_parser.add_argument('--json', action="store_true", help="Print result as JSON in stdout")
    arg_parser.add_argument('--verbose', action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument('--limit', type=int, default=None, help="Limit news topics if this parameter provided")
    arg_parser.add_argument('--date', type=str, default=None, help="Retrieves news for the date, format: 'YYYYMMDD'")
    arg_parser.add_argument('--to-html', action="store_true", help="Save result in HTML file")
    arg_parser.add_argument('--to-pdf', action="store_true", help="Save result in PDF file")
    arg_parser.add_argument('--colored', action="store_true", help="Print colored result")
    return arg_parser


def main():
    """Main function. Handle command-line arguments."""
    arg_parse = parse_cli_arguments()
    if len(sys.argv) == 1:
        arg_parse.print_usage()
        return
    cli_arguments = arg_parse.parse_args()
    sys.stdout = sys.__stdout__ if cli_arguments.verbose else io.StringIO()
    colored = None
    if cli_arguments.colored:
        import colors
        print_exception = colors.print_exceptions
        colored = colors
    else:
        print_exception = print
    try:
        reader = RSSReader(cli_arguments, colored)
        if cli_arguments.to_html:
            reader.convert2html()
        if cli_arguments.to_pdf:
            reader.convert2pdf()
    except Exception as e:
        sys.stdout = sys.__stdout__
        print_exception(e)
    else:
        sys.stdout = sys.__stdout__
        if cli_arguments.json:
            reader.print_json()
        else:
            reader.print_news()


if __name__ == "__main__":
    main()
