from urllib.parse import urlparse


class OutgoingRequest:
    def __init__(self, url, method, body=None):
        self.url = url
        self.method = method
        self.body = body

    @property
    def path(self):
        return urlparse(self.url).path
