from __future__ import unicode_literals
from .responses import Route53Response

url_bases = [
    "https?://route53(.*).amazonaws.com",
]

url_paths = {
    '{0}/$': IamResponse.dispatch,
}

