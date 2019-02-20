# #!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mock
import unittest
import requests
from requests.exceptions import HTTPError

from moto.packages.httpretty.core import HTTPrettyRequest

"""
example text that mocks requests.get and
returns a mock Response object
"""


def _mock_response(
        status=200,
        content="CONTENT",
        json_data=None,
        raise_for_status=None):
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """
    mock_resp = mock.Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    # add json data if provided
    if json_data:
        mock_resp.json = mock.Mock(
            return_value=json_data
        )
    return mock_resp

@mock.patch('requests.get')
def test_parse_querystring( mock_get):
    mock_resp = _mock_response(status=500, raise_for_status=HTTPError("google is down"))
    mock_get.return_value = mock_resp


    headers = 'User-Agent=Boto3/1.9.90 Python/3.6.0 Darwin/18.2.0 Botocore/1.12.90'
    core = HTTPrettyRequest(headers=headers)
