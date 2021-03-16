import requests
from bs4 import BeautifulSoup
import colorama
import wikipedia
from collections import deque

class Browser:
    tabs = dict()
    history = deque()

    details = {"Who am I?": "Elugubanti",
                "What am I?":   "A text-based browser",
                "Who pets me?": "Ravi Chandra N Reddy",
                "How old am I?": "Just a few hours"}
    
    def __init__(self):
        colorama.init()

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
                if tag.name == 'a':
                    page_content += colorama.Fore.BLUE + tag.text + '\n'
                elif tag.name in tags and tag.name != 'a':
                    page_content += colorama.Fore.WHITE + tag.text + '\n'
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

def main():
    browser_instance = Browser()
    while True:
        input_url = input()
        if input_url == "exit":
            browser_instance.close_browser()
        elif input_url == "about":
            for key in browser_instance.details:
                print(key, ":", browser_instance.details[key])
        elif input_url == "back":
            if not browser_instance.history:
                browser_instance.close_browser()
            elif len(browser_instance.history) == 1:
                browser_instance.history.pop()
                browser_instance.display("Your history is Empty")
            else:
                    browser_instance.history.pop()
                    previous_page = browser_instance.history.pop()
                    browser_instance.display(browser_instance.read_page_from_cache(previous_page))
                    browser_instance.history.append(previous_page)
        elif input_url == "switch tabs":
            if not browser_instance.history:
                browser_instance.display("No other tabs open")
            else:
                browser_instance.switch()
                continue
        elif "." not in input_url:
            browser_instance.wiki(input_url)
        else:
            if input_url.startswith("http://"):
                input_url = input_url[len("http://"):]
            if not input_url.startswith("https://"):
                input_url = "https://" + input_url
            if input_url in browser_instance.history:
                page_content = browser_instance.read_page_from_cache(input_url)
                browser_instance.display(page_content)
                browser_instance.history.append(input_url)
            else:
                r = requests.get(input_url)
                page_content = browser_instance.parse_text_from_page(r)
                browser_instance.display(page_content)
                browser_instance.write_page_to_cache(input_url, page_content)
                browser_instance.history.append(input_url)

if __name__ == "__main__":
    main()
