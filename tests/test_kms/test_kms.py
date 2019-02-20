from __future__ import unicode_literals

import boto3
from moto import mock_kms, mock_kms_deprecated


import logging
from inspect import currentframe
import inspect

logging.basicConfig(filename='/tmp/models.log',level=logging.DEBUG)

logger = logging.getLogger(__name__)


DEBUG=1

def get_linenumber():
    cf = currentframe()
    return " - "+str(cf.f_back.f_lineno)

@mock_kms
def test_create_key():
    client = boto3.client('kms', region_name='us-east-1')
    key = client.create_key(Description='cancel-key-deletion')
    response = client.schedule_key_deletion(
        KeyId=key['KeyMetadata']['KeyId']
    )

    if DEBUG:
        logging.debug('models.py - KmsBackend(BaseBackend) create_key - '
                      ' -caller: ' + str(
            inspect.stack()[1][3]) + "-" + get_linenumber())

        logging.debug('response: '+str(response))

    keyid = response['KeyId']
    response = client.tag_resource(
        KeyId=keyid,
        Tags=[
            {
                'TagKey': 'string',
                'TagValue': 'string'
            },
        ]
    )

    #response = client.list_resource_tags(
    #    KeyId=keyid
    #)

    assert response == 'test'


    #def tag_resource(self):
    #    key_id = self.parameters.get('KeyId')
    #    tags = self.parameters.get('Tags')
    #    self.kms_backend.tag_resource(key_id,tags)
    #    return json.dumps({})

