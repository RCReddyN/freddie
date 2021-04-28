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

        self.content_box = tk.Text(self)
        self.content_box.pack(side = "bottom")

        self.scroll = tk.Scrollbar(self)
        self.scroll["command"] = self.content_box.yview

        self.content_box["yscrollcommand"]=self.scroll.set

    def set_content(self):
        self.content_box.insert(tk.END, self.get_content())

    def get_url(self):
        self.content_box.delete(1.0, tk.END)
        return self.url_box.get()

    def get_content(self):
        input_url = self.get_url()
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
root.title("Freddie")
root.state("zoomed")
app = Freddie(master=root)
app.mainloop()