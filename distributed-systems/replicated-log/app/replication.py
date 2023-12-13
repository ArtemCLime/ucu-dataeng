import gevent
from gevent import monkey

monkey.patch_all()
import requests
import logging
from tenacity import retry, wait_exponential, before_sleep_log
from utils import timeit
import sys

from logger import get_logger

logger = get_logger()


class ReplicationHandler:
    def __init__(self, servers, is_master=False):
        self.servers = servers
        self.is_master = is_master

    def replicate(self, message, write_concern):
        if not self.is_master:
            return
        jobs = [
            gevent.spawn(self._replicate, message, server) for server in self.servers
        ]

        # Wait for all servers to replicate
        done_jobs = gevent.wait(jobs, count=write_concern - 1)
        if done_jobs:
            logger.info(f"[{timeit()}] [DONE] Done jobs {done_jobs}")
            return True
        return False

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def _replicate(self, message, server):
        url = f"http://{server['host']}:{server['port']}/replicate"
        params = message.to_json()
        response = requests.post(url, params=params, timeout=1)
        response.raise_for_status()
        logger.info(
            f"[SERVER] [{timeit()}] Server {server['host']}:{server['port']} replicated message {message}"
        )
        return True
