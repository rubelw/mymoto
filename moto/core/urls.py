from __future__ import unicode_literals
from .responses import MotoAPIResponse

url_bases = [
    "https?://motoapi.amazonaws.com"
]

response_instance = MotoAPIResponse()

url_paths = {
    '{0}/moto-api/$': response_instance.dashboard,
    '{0}/moto-api/data.json': response_instance.model_data,
    '{0}/moto-api/reset': response_instance.reset_response,
}
