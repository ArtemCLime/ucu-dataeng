import grequests
import logging

logger = logging.getLogger(__name__)


class ReplicationHandler:
    def __init__(self, servers, is_master=False):
        self.servers = servers
        self.is_master = is_master

    def replicate(self, message):
        if not self.is_master:
            return

        requests_list = [
           self._replicate(message, server) for server in self.servers
        ]

        responses = grequests.map(requests_list)
        self.parse_response(responses)
    
    def _replicate(self, message, server):
        url = f"http://{server['host']}:{server['port']}/replicate"
        params = {"message": message}
        return grequests.post(url, params=params)

    def parse_response(self, responses):
        for response in responses:
            if (not response) or response.status_code != 200:
                print(f"Failed to replicate message to {response.url}")
            else:
                print(f"Successfully replicated message to {response.url}")
