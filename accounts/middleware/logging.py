import logging
import time
from turtle import st

from django.template import RequestContext

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s; %(message)s")
handler.formatter = formatter
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# Logger(level=logging.INFO)


class LoggingMiddelware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        #code before request process
        start_time = time.time()
        request_data = {
            'method': request.method,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'path': request.path,
        }
        logger.info(request_data)

        response = self.get_response(request)
        duration = time.time() - start_time
        response_dict = {
            'status_code':response.status_code,
            'duration':duration,
        }
        
        logger.info(response_dict)
        #code before request process
        return response