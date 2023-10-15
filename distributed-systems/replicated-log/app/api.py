#### Master API for Replicated Log Application

import fastapi
from log import MessageLog
from replication import ReplicationHandler
import json
import argparse
import os
import uvicorn

is_master = os.environ.get('IS_MASTER', False)
servers = os.environ.get('SERVERS', [])
port = os.environ.get('APP_PORT', 8000)

app = fastapi.FastAPI()
log = MessageLog()
replicator = ReplicationHandler(
    servers=servers,
    host='localhost',
    port=port
)


# GET Method: returns all messages in the log
@app.get("/log")
def get_log():
    return {"log": log.get_all_messages()}


# POST Method: appends a message to the log
@app.post("/log")
def post_log(message: str):
    log.append(message)
    replicator.replicate(message)
    return {"msg": "Message added to log"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=port)

