import requests
import gevent
import logging
from tenacity import retry

logger = logging.getLogger(__name__)


class ReplicationHandler:
    def __init__(self, servers, is_master=False):
        self.servers = servers
        self.is_master = is_master

    def replicate(self, message, write_concern):
        if not self.is_master:
            return
        if write_concern == 1:
            return True
        
        jobs = [gevent.spawn(self._replicate, message, server) for server in self.servers]

        with gevent.iwait(jobs) as it:
            for i in it:
                if (i.exception is None) and (i.value):
                    write_concern -= 1
                if write_concern == 1:
                    return True
        return False
                
    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def _replicate(self, message, server):
        url = f"http://{server['host']}:{server['port']}/replicate"
        params = {"message": message}
        return self.parse_response(requests.post(url, params=params))

    def parse_response(self, response):
        if (not response) or response.status_code != 200:
            print(f"Failed to replicate message to {response.url}")
            raise Exception(f"Failed to replicate message to {response.url}")
        else:
            return True
