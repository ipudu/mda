import base64
import re
import sys
import subprocess
import requests

from bs4 import BeautifulSoup as BSHTML
from io import BytesIO
from PIL import Image
from retrying import retry
import tkinter as tk

SCIHUB = "http://sci-hub.tw/"


class Paper:
    def __init__(self, identifer):

        # save captcha string
        self.captcha = ""

        self.flag = True

        if not self.paper_check(identifer):
            self.flag = False
        else:
            self.identifer = identifer
            self.fetch()

    def fetch(self):
        URL = SCIHUB + self.identifer
        resp = requests.get(URL)
        link = re.search(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+pdf",
            resp.text,
        )
        if link:
            pdf_link = link.group(0)
        else:
            link = re.search(
                "//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+pdf",
                resp.text,
            )
            pdf_link = "http:" + link.group(0)

        self.process(pdf_link)

    def process(self, url):
        while True:
            resp = requests.get(url)
            if "text/html" in resp.headers["content-type"]:
                html = resp.text
                print(html)
            else:
                self.download(url)
                return

            # get image url
            soup = BSHTML(html, "html.parser")
            image = soup.findAll("img")
            image_url = resp.cookies.list_domains()[0] + image[0]["src"]

            self.gui(image_url)
            os.remove("captcha.png")

            payload = {"answer": self.captcha}

            r = requests.post(url, params=payload)

    def gui(self, url):
        if not url.startswith("http://"):
            url = "http://" + url
        resp = requests.get(url)
        img = Image.open(BytesIO(resp.content))
        img.save("captcha.png")

        def getText():
            # You can perform check on some condition if you want to
            # If it is okay, then store the value, and exist
            self.captcha = inputBox.get()
            print("User entered captcha: ", self.captcha)
            root.destroy()

        root = tk.Tk()
        simpleTitle = tk.Label(root)
        simpleTitle["text"] = "CAPTCHA"
        simpleTitle.pack()

        # The image (but in the label widget)
        img = tk.PhotoImage(file="captcha.png")
        imageLabel = tk.Label(image=img)
        imageLabel.pack()

        # The entry box widget
        inputBox = tk.Entry(root)
        inputBox.pack()

        # The button widget
        button = tk.Button(root, text="Submit", command=getText)
        button.pack()

        tk.mainloop()

    @retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=10)
    def download(self, link):
        print("Downloading paper...")
        subprocess.run(["curl", "-O", link])

    def paper_check(self, identifer):

        # check if identifer is URL
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        # check if identifer is DOI
        # FIXME: get correct regex
        DOI = re.compile(r"^10.*/.*", re.IGNORECASE)

        return True if re.match(regex, identifer) or re.match(DOI, identifer) else False
