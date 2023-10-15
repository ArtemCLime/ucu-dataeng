import requests
import logging
import logging

logger = logging.getLogger(__name__)


class ReplicationHandler:
    def __init__(self, servers, is_master=False):
        self.servers = servers
        self.is_master = is_master

    def replicate(self, message):
        if not self.is_master:
            return
        for server in self.servers:
            r = requests.post(
                f"http://{server['host']}:{server['port']}/replicate",
                params={"message": message},
            )
            if r.status_code != 200:
                print(
                    f"Failed to replicate message to {server['host']}:{server['port']}"
                )
            else:
                print(
                    f"Successfully replicated message to {server['host']}:{server['port']}"
                )
