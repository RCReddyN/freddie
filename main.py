from support.browser import Browser
import requests
import wikipedia
import tkinter as tk

class Freddie(tk.Frame):

    browser_instance = Browser()

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.url_box = tk.Entry(self)
        self.url_box.pack(side="left")
        self.get_button = tk.Button(self)
        self.get_button["text"] = "Get"
        self.get_button["command"] = self.set_content
        self.get_button.pack(side="left")

        self.get_button["command"] = self.set_content
        self.get_button.pack(side="left")
        self.content_box = tk.Message(self)
        self.content_box.pack(side = "bottom")
    
    def set_content(self):
        self.content_box["text"] = self.get_content()

    def get_content(self):
        input_url = "google.com"
        if "." in input_url:
            if input_url.startswith("http://"):
                input_url = input_url[len("http://"):]
            if not input_url.startswith("https://"):
                input_url = "https://" + input_url
            if input_url in self.browser_instance.history:
                page_content = self.browser_instance.read_page_from_cache(input_url)
                return (page_content)
                self.browser_instance.history.append(input_url)
            else:
                r = requests.get(input_url)
                page_content = self.browser_instance.parse_text_from_page(r)
                return (page_content)
                self.browser_instance.write_page_to_cache(input_url, page_content)
                self.browser_instance.history.append(input_url)
        return "Not a valid url!"
root = tk.Tk()
app = Freddie(master=root)
app.mainloop()