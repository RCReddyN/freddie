from support.browser import Browser
import requests
import wikipedia
import tkinter as tk


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
            browser_instance.display("Not a valid URL!")
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

main()