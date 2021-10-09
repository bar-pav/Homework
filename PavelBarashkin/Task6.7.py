import math
import re


class Pagination:
    def __init__(self, text, symbols_per_page):
        self.__text = text
        self.item_count = len(text)
        self.__symbols_per_page = symbols_per_page
        self.page_count = math.ceil(self.item_count / self.__symbols_per_page)
        self.__pages = [(i * self.__symbols_per_page, i * self.__symbols_per_page + self.__symbols_per_page) for i in
                        range(self.page_count)]

    def count_items_on_page(self, page):
        if page < (len(self.__pages) - 1):
            print(self.__symbols_per_page)
        elif page == len(self.__pages) - 1:
            print(len(self.__text[self.__pages[-1][0]:self.__pages[-1][1]]))
        else:
            print("Exception: Invalid index. Page is missing")

    def find_page(self, string):
        results = re.finditer('{}'.format(string).format(string), self.__text)
        find_on_pages = [None]
        for i in results:
            for page in self.__pages[i.span()[0] // self.__symbols_per_page: (i.span()[1] - 1) // self.__symbols_per_page + 1]:
                if (page[0] // self.__symbols_per_page) == find_on_pages[-1]:
                    continue
                else:
                    find_on_pages.append(page[0] // self.__symbols_per_page)
        if len(find_on_pages) > 1:
            print(find_on_pages[1:])
        else:
            print(f"Exception: '{string}' is missing on the pages")

    def display_page(self, number):
        if number > len(self.__pages) - 1 or number < 0:
            print(f"Page range 0-{len(self.__pages) - 1}")
        else:
            print(self.__text[self.__pages[number][0]:self.__pages[number][1]])


pages = Pagination('Your beautiful text', 5)
print(pages.page_count)
print(pages.item_count)
pages.count_items_on_page(0)
pages.count_items_on_page(3)
pages.count_items_on_page(4)
pages.find_page('beautiful')
pages.find_page('great')
pages.display_page(0)
pages.display_page(3)
pages.display_page(4)
