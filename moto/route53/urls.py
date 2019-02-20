from __future__ import unicode_literals
from .responses import Route53
import logging
from inspect import currentframe
import inspect

logging.basicConfig(filename='/tmp/models.log',level=logging.DEBUG)

logger = logging.getLogger(__name__)


DEBUG=1

def get_linenumber():
    cf = currentframe()
    return " - "+str(cf.f_back.f_lineno)

url_bases = [
    "https?://route53(.*).amazonaws.com",
]


def tag_response1(*args, **kwargs):
    if DEBUG:
        logging.debug('urls.py - route53 - tag_response1 -caller: ' + str(inspect.stack()[1][3]) + "-" + get_linenumber())


    return Route53().list_or_change_tags_for_resource_request(*args, **kwargs)


def tag_response2(*args, **kwargs):
    if DEBUG:
        logging.debug('urls.py - route53 - tag_response2 -caller: ' + str(inspect.stack()[1][3]) + "-" + get_linenumber())


    return Route53().list_or_change_tags_for_resource_request(*args, **kwargs)


url_paths = {
    '{0}/(?P<api_version>[\d_-]+)/change/(?P<zone_id>[^/]+)$': Route53().get_change,
    '{0}/(?P<api_version>[\d_-]+)/hostedzone$': Route53().list_or_create_hostzone_response,
    '{0}/(?P<api_version>[\d_-]+)/hostedzone/(?P<zone_id>[^/]+)$': Route53().get_or_delete_hostzone_response,
    '{0}/(?P<api_version>[\d_-]+)/hostedzone/(?P<zone_id>[^/]+)/rrset/?$': Route53().rrset_response,
    '{0}/(?P<api_version>[\d_-]+)/hostedzonesbyname': Route53().list_hosted_zones_by_name_response,
    '{0}/(?P<api_version>[\d_-]+)/healthcheck': Route53().health_check_response,
    '{0}/(?P<api_version>[\d_-]+)/tags/healthcheck/(?P<zone_id>[^/]+)$': tag_response1,
    '{0}/(?P<api_version>[\d_-]+)/tags/hostedzone/(?P<zone_id>[^/]+)$': tag_response2,
    '{0}/(?P<api_version>[\d_-]+)/trafficpolicyinstances/*': Route53().not_implemented_response
}
