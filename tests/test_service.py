import unittest

from unittest.mock import Mock, patch

from .tools import mock_request
from xmlcatalog import service
from pywoo import Api

class TestService(unittest.TestCase):

    @patch('pywoo.pywoo.requests.api.request', side_effect=mock_request)
    def test_service(self, func):
        service.create_xml()
