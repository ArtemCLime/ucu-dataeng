# COnfiguration variables for the app
import os

PORT = os.environ.get("APP_PORT", 8000)
IS_MASTER = bool(os.environ.get("IS_MASTER", False))
IS_BROKEN = bool(os.environ.get("IS_BROKEN", False))
NAME = os.environ.get("NAME", "master")

SERVERS = [{"host": "app2", "port": 8001}, {"host": "app3", "port": 8002}]

MAX_SLEEP_TIME = 5
FAIL_PROBABILITY = 0.1
SLEEP_PROBABILITY = 0.2
