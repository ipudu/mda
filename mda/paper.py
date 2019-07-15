import re
import sys
import subprocess
import requests

from retrying import retry

SCIHUB = "http://sci-hub.tw/"

class Paper:
    def __init__(self, identifer):

        self.flag = True
        
        if not self.paper_check(identifer):
            self.flag = False
        else:
            self.identifer = identifer
            self.fetch()
    
    def fetch(self):
        URL = SCIHUB + self.identifer
        resp = requests.get(URL)
        pdf_link = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+pdf', resp.text)
        if pdf_link:
            self.download(pdf_link.group(0))
        else:
            pdf_link = re.search('//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+pdf', resp.text)
            self.download('http:'+pdf_link.group(0))

    @retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=10)
    def download(self, link):
        print('Downloading paper...')
        subprocess.run(['curl', '-O', link])

    def paper_check(self, identifer):

        # check if identifer is URL
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        # check if identifer is DOI
        # FIXME: get correct regex
        DOI = re.compile(r'^10.*/.*', re.IGNORECASE)

        return True if re.match(regex, identifer) or re.match(DOI, identifer) else False