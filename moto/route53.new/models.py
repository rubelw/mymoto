from __future__ import unicode_literals

from collections import defaultdict

import string
import random
import uuid
import json
from jinja2 import Template
from datetime import datetime
from pprint import pprint
from moto.core import BaseBackend, BaseModel

import logging
from inspect import currentframe
import inspect

logging.basicConfig(filename='/tmp/models.log',level=logging.DEBUG)

logger = logging.getLogger(__name__)


DEBUG=1

def get_linenumber():
    cf = currentframe()
    return " - "+str(cf.f_back.f_lineno)

ROUTE53_ID_CHOICE = string.ascii_uppercase + string.digits


def create_route53_zone_id():
    if DEBUG:
        logging.debug('models.py - route53 - create_route53_zone_id -caller: ' + str(inspect.stack()[1][3]) + "-" + get_linenumber())

    # New ID's look like this Z1RWWTK7Y8UDDQ
    return ''.join([random.choice(ROUTE53_ID_CHOICE) for _ in range(0, 15)])


class HealthCheck(BaseModel):

    def __init__(self, health_check_id, health_check_args):

        if DEBUG:
            logging.debug('models.py - HealthCheck(BaseModel) __init__ -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())


        self.id = health_check_id
        self.ip_address = health_check_args.get("ip_address")
        self.port = health_check_args.get("port", 80)
        self._type = health_check_args.get("type")
        self.resource_path = health_check_args.get("resource_path")
        self.fqdn = health_check_args.get("fqdn")
        self.search_string = health_check_args.get("search_string")
        self.request_interval = health_check_args.get("request_interval", 30)
        self.failure_threshold = health_check_args.get("failure_threshold", 3)
        self.tags = {}

    @property
    def physical_resource_id(self):
        if DEBUG:
            logging.debug('models.py - HealthCheck(BaseModel) physical_resource_id -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        return self.id

    @classmethod
    def create_from_cloudformation_json(cls, resource_name, cloudformation_json, region_name):

        if DEBUG:
            logging.debug('models.py - HealthCheck(BaseModel) create_from_cloudformation_json -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        properties = cloudformation_json['Properties']['HealthCheckConfig']
        health_check_args = {
            "ip_address": properties.get('IPAddress'),
            "port": properties.get('Port'),
            "type": properties['Type'],
            "resource_path": properties.get('ResourcePath'),
            "fqdn": properties.get('FullyQualifiedDomainName'),
            "search_string": properties.get('SearchString'),
            "request_interval": properties.get('RequestInterval'),
            "failure_threshold": properties.get('FailureThreshold'),
        }
        health_check = route53_backend.create_health_check(health_check_args)
        return health_check

    def to_xml(self):

        if DEBUG:
            logging.debug('models.py - HealthCheck(BaseModel) to_xml -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        template = Template("""<HealthCheck>
            <Id>{{ health_check.id }}</Id>
            <CallerReference>example.com 192.0.2.17</CallerReference>
            <HealthCheckConfig>
                <IPAddress>{{ health_check.ip_address }}</IPAddress>
                <Port>{{ health_check.port }}</Port>
                <Type>{{ health_check._type }}</Type>
                <ResourcePath>{{ health_check.resource_path }}</ResourcePath>
                <FullyQualifiedDomainName>{{ health_check.fqdn }}</FullyQualifiedDomainName>
                <RequestInterval>{{ health_check.request_interval }}</RequestInterval>
                <FailureThreshold>{{ health_check.failure_threshold }}</FailureThreshold>
                {% if health_check.search_string %}
                    <SearchString>{{ health_check.search_string }}</SearchString>
                {% endif %}
            </HealthCheckConfig>
            <HealthCheckVersion>1</HealthCheckVersion>
        </HealthCheck>""")
        return template.render(health_check=self)


class RecordSet(BaseModel):

    def __init__(self, kwargs):

        if DEBUG:
            logging.debug('models.py - RecordSet(BaseModel) __init__ -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        self.name = kwargs.get('Name')
        self._type = kwargs.get('Type')
        self.ttl = kwargs.get('TTL')
        self.records = kwargs.get('ResourceRecords', [])
        self.set_identifier = kwargs.get('SetIdentifier')
        self.weight = kwargs.get('Weight')
        self.region = kwargs.get('Region')
        self.health_check = kwargs.get('HealthCheckId')
        self.hosted_zone_name = kwargs.get('HostedZoneName')
        self.hosted_zone_id = kwargs.get('HostedZoneId')

    @classmethod
    def create_from_cloudformation_json(cls, resource_name, cloudformation_json, region_name):

        if DEBUG:
            logging.debug('models.py - RecordSet(BaseModel) create_from_cloudformation_json -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        properties = cloudformation_json['Properties']

        zone_name = properties.get("HostedZoneName")
        if zone_name:
            hosted_zone = route53_backend.get_hosted_zone_by_name(zone_name)
        else:
            hosted_zone = route53_backend.get_hosted_zone(
                properties["HostedZoneId"])
        record_set = hosted_zone.add_rrset(properties)
        return record_set

    @classmethod
    def update_from_cloudformation_json(cls, original_resource, new_resource_name, cloudformation_json, region_name):
        cls.delete_from_cloudformation_json(
            original_resource.name, cloudformation_json, region_name)
        return cls.create_from_cloudformation_json(new_resource_name, cloudformation_json, region_name)

    @classmethod
    def delete_from_cloudformation_json(cls, resource_name, cloudformation_json, region_name):
        # this will break if you changed the zone the record is in,
        # unfortunately
        properties = cloudformation_json['Properties']

        zone_name = properties.get("HostedZoneName")
        if zone_name:
            hosted_zone = route53_backend.get_hosted_zone_by_name(zone_name)
        else:
            hosted_zone = route53_backend.get_hosted_zone(
                properties["HostedZoneId"])

        try:
            hosted_zone.delete_rrset_by_name(resource_name)
        except KeyError:
            pass

    @property
    def physical_resource_id(self):

        if DEBUG:
            logging.debug('models.py - RecordSet(BaseModel) physical_resource_id -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        return self.name

    def to_xml(self):
        template = Template("""<ResourceRecordSet>
                <Name>{{ record_set.name }}</Name>
                <Type>{{ record_set._type }}</Type>
                {% if record_set.set_identifier %}
                    <SetIdentifier>{{ record_set.set_identifier }}</SetIdentifier>
                {% endif %}
                {% if record_set.weight %}
                    <Weight>{{ record_set.weight }}</Weight>
                {% endif %}
                {% if record_set.region %}
                    <Region>{{ record_set.region }}</Region>
                {% endif %}
                {% if record_set.ttl %}
                    <TTL>{{ record_set.ttl }}</TTL>
                {% endif %}
                <ResourceRecords>
                    {% for record in record_set.records %}
                    <ResourceRecord>
                        <Value>{{ record }}</Value>
                    </ResourceRecord>
                    {% endfor %}
                </ResourceRecords>
                {% if record_set.health_check %}
                    <HealthCheckId>{{ record_set.health_check }}</HealthCheckId>
                {% endif %}
            </ResourceRecordSet>""")
        return template.render(record_set=self)

    def delete(self, *args, **kwargs):

        if DEBUG:
            logging.debug('models.py - RecordSet(BaseModel) delete -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        ''' Not exposed as part of the Route 53 API - used for CloudFormation. args are ignored '''
        hosted_zone = route53_backend.get_hosted_zone_by_name(
            self.hosted_zone_name)
        if not hosted_zone:
            hosted_zone = route53_backend.get_hosted_zone(self.hosted_zone_id)
        hosted_zone.delete_rrset_by_name(self.name)


class FakeZone(BaseModel):

    def __init__(self, name, id_, private_zone, comment=None):

        if DEBUG:
            logging.debug('models.py -FakeZone(BaseModel) __init__ -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        self.name = name
        self.id = id_
        if comment is not None:
            self.comment = comment
        self.private_zone = private_zone
        self.rrsets = []
        self.tags = {}
        self.create_date = datetime.strftime(
            datetime.utcnow(),
            "%Y-%m-%dT%H:%M:%SZ"
        )


        if DEBUG:
            logging.debug(vars(self))


    def add_rrset(self, record_set):

        if DEBUG:
            logging.debug('models.py -FakeZone(BaseModel) add_rrset -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        record_set = RecordSet(record_set)
        self.rrsets.append(record_set)
        return record_set

    def upsert_rrset(self, record_set):

        if DEBUG:
            logging.debug('models.py -FakeZone(BaseModel) upsert_rrset -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        new_rrset = RecordSet(record_set)
        for i, rrset in enumerate(self.rrsets):
            if rrset.name == new_rrset.name:
                self.rrsets[i] = new_rrset
                break
        else:
            self.rrsets.append(new_rrset)
        return new_rrset

    def delete_rrset_by_name(self, name):

        if DEBUG:
            logging.debug('models.py -FakeZone(BaseModel) delete_rrset_by_name -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        self.rrsets = [
            record_set for record_set in self.rrsets if record_set.name != name]

    def delete_rrset_by_id(self, set_identifier):

        if DEBUG:
            logging.debug('models.py -FakeZone(BaseModel) delete_rrset_by_id -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        self.rrsets = [
            record_set for record_set in self.rrsets if record_set.set_identifier != set_identifier]

    def get_record_sets(self, start_type, start_name):

        if DEBUG:
            logging.debug('models.py -FakeZone(BaseModel) get_record_sets -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        record_sets = list(self.rrsets)  # Copy the list
        if start_type:
            record_sets = [
                record_set for record_set in record_sets if record_set._type >= start_type]
        if start_name:
            record_sets = [
                record_set for record_set in record_sets if record_set.name >= start_name]

        return record_sets

    @property
    def physical_resource_id(self):
        return self.id

    @classmethod
    def create_from_cloudformation_json(cls, resource_name, cloudformation_json, region_name):
        properties = cloudformation_json['Properties']
        name = properties["Name"]

        hosted_zone = route53_backend.create_hosted_zone(
            name, private_zone=False)
        return hosted_zone


class RecordSetGroup(BaseModel):

    def __init__(self, hosted_zone_id, record_sets):

        if DEBUG:
            logging.debug('models.py -RecordSetGroup(BaseModel) __init__ -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        self.hosted_zone_id = hosted_zone_id
        self.record_sets = record_sets

    @property
    def physical_resource_id(self):
        return "arn:aws:route53:::hostedzone/{0}".format(self.hosted_zone_id)

    @classmethod
    def create_from_cloudformation_json(cls, resource_name, cloudformation_json, region_name):
        properties = cloudformation_json['Properties']

        zone_name = properties.get("HostedZoneName")
        if zone_name:
            hosted_zone = route53_backend.get_hosted_zone_by_name(zone_name)
        else:
            hosted_zone = route53_backend.get_hosted_zone(properties["HostedZoneId"])
        record_sets = properties["RecordSets"]
        for record_set in record_sets:
            hosted_zone.add_rrset(record_set)

        record_set_group = RecordSetGroup(hosted_zone.id, record_sets)
        return record_set_group


class Route53Backend(BaseBackend):

    def __init__(self):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) __init__ -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        self.zones = {}
        self.health_checks = {}
        self.resource_tags = defaultdict(dict)

    def create_hosted_zone(self, name, private_zone, comment=None):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) create_hosted_zone -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        new_id = create_route53_zone_id()
        new_zone = FakeZone(
            name, new_id, private_zone=private_zone, comment=comment)
        self.zones[new_id] = new_zone
        return new_zone

    def change_tags_for_resource(self, resource_id, tags):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) change_tags_for_resource -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        if 'Tag' in tags:
            if isinstance(tags['Tag'], list):
                for tag in tags['Tag']:
                    self.resource_tags[resource_id][tag['Key']] = tag['Value']
            else:
                key, value = (tags['Tag']['Key'], tags['Tag']['Value'])
                self.resource_tags[resource_id][key] = value
        else:
            if 'Key' in tags:
                if isinstance(tags['Key'], list):
                    for key in tags['Key']:
                        del(self.resource_tags[resource_id][key])
                else:
                    del(self.resource_tags[resource_id][tags['Key']])

    def list_tags_for_resource(self, resource_id):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) list_tags_for_resource -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        if resource_id in self.resource_tags:
            return self.resource_tags[resource_id]

    def get_all_hosted_zones(self):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) get_all_hosted_zones -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        # Returns an array of the values in the zone
        return self.zones.values()

    def get_hosted_zone(self, id_):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) get_hosted_zone -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        return self.zones.get(id_.replace("/hostedzone/", ""))


    def get_hosted_zone_by_id(self, id):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) get_hosted_zone_by_id -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        for zone in self.get_all_hosted_zones():
            if zone.id == id:
                return zone

    def get_hosted_zone_by_name(self, name):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) get_hosted_zone_by_name -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        for zone in self.get_all_hosted_zones():
            if zone.name == name:
                return zone

    def delete_hosted_zone(self, id_):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) delete_hosted_zone -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        return self.zones.pop(id_.replace("/hostedzone/", ""), None)

    def create_health_check(self, health_check_args):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) create_health_check -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        health_check_id = str(uuid.uuid4())
        health_check = HealthCheck(health_check_id, health_check_args)
        self.health_checks[health_check_id] = health_check
        return health_check

    def get_health_checks_by_id(self, id):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) get_health_check_by_id -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        for checks in self.get_health_checks():
            if checks.id == id:
                return checks


    def get_health_checks(self):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) get_health_check -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        # Returns an array of the values in healthchecks dict
        return self.health_checks.values()

    def delete_health_check(self, health_check_id):

        if DEBUG:
            logging.debug('models.py -Route53Backend(BaseModel) delete_health_check -caller: ' + str(
                inspect.stack()[1][3]) + "-" + get_linenumber())

        return self.health_checks.pop(health_check_id, None)


route53_backend = Route53Backend()
