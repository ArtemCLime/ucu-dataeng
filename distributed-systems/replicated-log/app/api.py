#### Master API for Replicated Log Application

import fastapi
from log import MessageLog
from replication import ReplicationHandler
import json
import argparse
import os
import uvicorn
from time import sleep
import logging
import random

port = os.environ.get("APP_PORT", 8000)
is_master = bool(os.environ.get("IS_MASTER", False))
is_broken = bool(os.environ.get("IS_BROKEN", False))
name = os.environ.get("NAME", "master")

logger = logging.getLogger(__name__)

servers = [{"host": "app2", "port": 8001}, {"host": "app3", "port": 8002}]

app = fastapi.FastAPI()
log = MessageLog()
replicator = ReplicationHandler(servers=servers, is_master=is_master)


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
def post_log(message, write_concern):
    log.append(message)
    if replicator.replicate(message, write_concern=int(write_concern)):
        return {"msg": f"Message added to log, {message}"}
    else:
        return {"msg": f"Message added to log, {message}, but not replicated"}


@app.post("/replicate")
def replicate(message):
    if is_broken:
        # Try add server delay
        sleep_time = random.randint(0, 2)
        print(f"Server {name} is sleeping for {sleep_time} seconds")
        sleep(sleep_time)

        # 50% chance of crashing
        if bool(random.getrandbits(1)):
            raise fastapi.HTTPException(status_code=500, detail=f"Server {name} crashed!")

    log.append(message)
    return {"msg": f"Message added to log, {message}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port), log_level="debug", access_log=True)
