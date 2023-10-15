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

port = os.environ.get("APP_PORT", 8000)
is_master = bool(os.environ.get("IS_MASTER", False))

logger = logging.getLogger(__name__)

servers = [{"host": "app2", "port": 8001}, {"host": "app3", "port": 8002}]

app = fastapi.FastAPI()
log = MessageLog()
replicator = ReplicationHandler(servers=servers, is_master=is_master)


# GET Method: returns all messages in the log
@app.get("/log")
def get_log():
    return {"log": log.get_all_messages()}


# POST Method: appends a message to the log
@app.post("/log")
def post_log(message):
    log.append(message)
    replicator.replicate(message)
    return {"msg": f"Message added to log, {message}"}


@app.post("/replicate")
def replicate(message):
    log.append(message)
    return {"msg": f"Message added to log, {message}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port), log_level="debug", access_log=True)
