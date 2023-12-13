import random
from time import sleep
import fastapi
from utils import timeit


class ServerBreaker:
    def __init__(self, fail_probability=0.1, sleep_probability=0.2, max_sleep_time=2):
        self.fail_probability = fail_probability
        self.sleep_probability = sleep_probability
        self.max_sleep_time = max_sleep_time

    def break_server(self, name=""):
        fail_probability = random.uniform(0, 1)
        if fail_probability < self.fail_probability:
            print(f"[FAILED][{timeit()}] Server {name} crashed!")
            raise fastapi.HTTPException(status_code=500, detail=f"Server {name} crashed!")
        elif self.fail_probability <= fail_probability < (self.sleep_probability + self.fail_probability):
            sleep_time = random.randint(0, self.max_sleep_time)
            print(f"[SLEEP] [{timeit()}] Server {name} is sleeping for {sleep_time} seconds")
            sleep(sleep_time)
        else:
            print(f"[OK] [{timeit()}] Server {name} running without a failure!")
