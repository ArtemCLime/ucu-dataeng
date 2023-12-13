#### Master API for Replicated Log Application

import fastapi
from log import MessageLog
from replication import ReplicationHandler
from broken import ServerBreaker
import json
import argparse
import os
import uvicorn
from time import sleep
import logging
import random
from utils import timeit

port = os.environ.get("APP_PORT", 8000)
is_master = bool(os.environ.get("IS_MASTER", False))
is_broken = bool(os.environ.get("IS_BROKEN", False))
name = os.environ.get("NAME", "master")

logger = logging.getLogger(__name__)

servers = [{"host": "app2", "port": 8001}, {"host": "app3", "port": 8002}]

app = fastapi.FastAPI()
log = MessageLog()
replicator = ReplicationHandler(servers=servers, is_master=is_master)
breaker = ServerBreaker(fail_probability=0.1, sleep_probability=0.2, max_sleep_time=2)


# GET Method: returns all messages in the log
@app.get("/log")
def get_log():
    return {"log": log.get_all_messages()}


@app.delete("/log")
def clean_log():
    log.clean()
    return {"log": log.get_all_messages()}


# POST Method: appends a message to the log
@app.post("/log")
def post_log(message, write_concern: int = 1):
    print(f"[INFO] [{timeit()}] Server {name} received message {message}")
    log.append(message)
    if replicator.replicate(message, write_concern=int(write_concern)):
        return {"msg": f"Message added to log, {message}"}
    else:
        return {"msg": f"Message added to log, {message}, but not replicated"}


@app.post("/replicate")
def replicate(message):
    print(f"[INFO] [{timeit()}] Server {name} received message {message}")
    if is_broken:
       breaker.break_server(name)

    log.append(message)
    return {"msg": f"Message added to log, {message}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port), log_level="debug", access_log=True)
