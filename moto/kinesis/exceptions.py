from __future__ import unicode_literals

import json
from werkzeug.exceptions import BadRequest


class ResourceNotFoundError(BadRequest):

    def __init__(self, message):
        super(ResourceNotFoundError, self).__init__()
        self.description = json.dumps({
            "message": message,
            '__type': 'ResourceNotFoundException',
        })


class ResourceInUseError(BadRequest):

    def __init__(self, message):
        super(ResourceInUseError, self).__init__()
        self.description = json.dumps({
            "message": message,
            '__type': 'ResourceInUseException',
        })


class StreamNotFoundError(ResourceNotFoundError):

    def __init__(self, stream_name):
        super(StreamNotFoundError, self).__init__(
            'Stream {0} under account 123456789012 not found.'.format(stream_name))


class ShardNotFoundError(ResourceNotFoundError):

    def __init__(self, shard_id):
        super(ShardNotFoundError, self).__init__(
            'Shard {0} under account 123456789012 not found.'.format(shard_id))


class InvalidArgumentError(BadRequest):

    def __init__(self, message):
        super(InvalidArgumentError, self).__init__()
        self.description = json.dumps({
            "message": message,
            '__type': 'InvalidArgumentException',
        })
