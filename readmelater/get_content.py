import requests
from readability import Document


class UrlContent:
    def __init__(self, url):
        self.url = url
        self.doc: str = None
        self.title: str = None

    def load(self):
        response = requests.get(self.url)
        doc = Document(response.text)
        self.title = doc.title()
        self.doc = doc.summary()






