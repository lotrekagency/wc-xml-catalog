import unittest

from unittest.mock import Mock, patch

from .tools import mock_request
from xmlcatalog import service
from pywoo import Api

class TestCoupon(unittest.TestCase):

    @patch('pywoo.pywoo.requests.api.request', side_effect=mock_request)
    def test_api_v3(self, func):
        api = Api('fake_api_host/wp-json/wc/v3', 'fake_consumer_key', 'fake_consumer_secret')
        service.createXML(api)