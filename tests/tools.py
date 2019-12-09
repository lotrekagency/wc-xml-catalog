import json
import os

class MockResponse:
    def __init__(self, text, ok=True, status_code=200):
        self.text = text
        self.ok = ok
        self.status_code = status_code

    def json(self):
        return json.loads(self.text)


def mock_request(method, url, *args, **kwargs):
    try:
        file = open(os.path.join(*(['resources'] + url.split("/")[3:] + [('{0}_{1}.json').format(method.lower(), kwargs.get('params', None).get('page', ''))] )), 'r')
    except:
        return MockResponse(text='[]')
    response = MockResponse(file.read())
    file.close()
    return response