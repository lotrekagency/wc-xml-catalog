import json
import os
from urllib.parse import urlparse

class MockResponse:
    def __init__(self, text, ok=True, status_code=200):
        self.text = text
        self.ok = ok
        self.status_code = status_code

    def json(self):
        return json.loads(self.text)


def mock_request(method, url, *args, **kwargs):
    try:
        if 'page' in kwargs['params'] and kwargs['params']['page'] > 1:
            return MockResponse(text='[]')
        url = urlparse(url).path
        file = open(os.path.join(*(['resources'] + url.split("/")[4:] + ['get.json'])), 'r')
    except:
        return MockResponse(text='[]')
    response = MockResponse(file.read())
    file.close()
    return response
