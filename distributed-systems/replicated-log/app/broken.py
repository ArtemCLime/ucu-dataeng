import random
from time import sleep
import fastapi
from utils import timeit
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


class ServerBreaker:
    def __init__(self, fail_probability=0.1, sleep_probability=0.2, max_sleep_time=2):
        self.fail_probability = fail_probability
        self.sleep_probability = sleep_probability
        self.max_sleep_time = max_sleep_time

    def break_server(self, name=""):
        fail_probability = random.uniform(0, 1)
        if fail_probability < self.fail_probability:
            logger.info(f"[FAILED][{timeit()}] Server {name} crashed!")
            raise fastapi.HTTPException(
                status_code=500, detail=f"Server {name} crashed!"
            )
        elif (
            self.fail_probability
            <= fail_probability
            < (self.sleep_probability + self.fail_probability)
        ):
            sleep_time = random.randint(0, self.max_sleep_time)
            logger.info(
                f"[SLEEP] [{timeit()}] Server {name} is sleeping for {sleep_time} seconds"
            )
            sleep(sleep_time)
        else:
            logger.info(f"[OK] [{timeit()}] Server {name} running without a failure!")
