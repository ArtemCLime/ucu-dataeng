import gevent
from gevent import monkey

monkey.patch_all()
import requests
import logging
from tenacity import retry, wait_exponential, before_sleep_log
from utils import timeit
import sys
from queue import Queue

from logger import get_logger

logger = get_logger()


class ReplicationHandler:
    def __init__(self, servers, is_master=False):
        self.servers = servers
        self.is_master = is_master
        self.failed_tasks = Queue()

        # Start a greenlet to process failed tasks
        gevent.spawn(self.process_failed_tasks)

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

    def _replicate(self, message, server):
        @retry(
            wait=wait_exponential(multiplier=1, min=2, max=3),
            retry_error_callback=self.add_to_failed_tasks,
        )
        def _replicate_with_retry(self, message, server):
            url = f"http://{server['host']}:{server['port']}/replicate"
            params = message.to_json()
            response = requests.post(url, params=params, timeout=1)
            response.raise_for_status()
            logger.info(
                f"[SERVER] [{timeit()}] Server {server['host']}:{server['port']} replicated message {message}"
            )
            return True

        return _replicate_with_retry(self, message, server)

    def is_server_up(self, server):
        url = f"http://{server['host']}:{server['port']}/health"
        try:
            response = requests.get(url, timeout=1)
            response.raise_for_status()
            logger.info(
                f"[SERVER] [{timeit()}] Server {server['host']}:{server['port']} is up"
            )
            return True
        except:
            logger.info(
                f"[SERVER] [{timeit()}] Server {server['host']}:{server['port']} is down"
            )
            return False

    def add_to_failed_tasks(self, retry_state):
        logger.info(
            f"[SERVER] [{timeit()}] Message [{message}] not delivered to {server['host']}:{server['port']}. Adding to failed tasks"
        )
        self.failed_tasks.put(retry_state.args)

    def process_failed_tasks(self):
        while True:
            # Get a failed task from the queue
            task = self.failed_tasks.get()

            # Check if the server is up
            if self.is_server_up(task[1]):
                # Try to process the failed task again
                try:
                    self._replicate(*task)
                except:
                    # If the task fails again, add it back to the queue
                    self.failed_tasks.put(task)
            else:
                # If the server is not up, add the task back to the queue
                self.failed_tasks.put(task)

            # Sleep for a while before processing the next task
            gevent.sleep(1)
