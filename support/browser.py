import requests
from bs4 import BeautifulSoup
import wikipedia
from collections import deque

class Browser:

    def __init__(self):
        self.tabs = dict()
        self.history = []
    
    def read_page_from_cache(self, page):
        self.display(self.tabs[page])

    def write_page_to_cache(self, page, page_content):
        self.tabs[page] = page_content

    def parse_text_from_page(self, r):
        if r.status_code == 200:
            page_content = ''
            soup = BeautifulSoup(r.content, 'html.parser')
            tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'al', 'li']
            for tag in soup.find_all(tags):
                if tag.name in tags:
                    page_content += tag.text + '\n'
            return page_content
        elif r.status_code == 404:
            return "404, Page Not Found"
        elif r.status_code == 410:
            return "410, Page Gone"
        elif r.status_code == 500:
            return "Internal Server Error"
        elif r.status_code == 503:
            return "Service Unavailable"
        else:
            if r.status_code // 100 != 3:
                return str(r.status_code) + ", Error" 
    
    def display(self, page_content):
        print(page_content + "\n")
    
    def close_browser(self):
        exit()

    def wiki(self, query):
        self.display(wikipedia.summary(query))

    def switch(self):
        for tab in self.history:
            self.display(tab)


