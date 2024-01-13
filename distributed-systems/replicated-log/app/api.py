#### API for Replicated Log Application
import fastapi
from log import MessageLog, Message
from replication import ReplicationHandler
from broken import ServerBreaker
import uvicorn
from utils import timeit

from logger import get_logger

logger = get_logger()

import config

app = fastapi.FastAPI()
log = MessageLog()
replicator = ReplicationHandler(servers=config.SERVERS, is_master=config.IS_MASTER)
breaker = ServerBreaker(
    fail_probability=config.FAIL_PROBABILITY,
    sleep_probability=config.SLEEP_PROBABILITY,
    max_sleep_time=config.MAX_SLEEP_TIME,
)


# GET Method: returns all messages in the log
@app.get("/log")
def get_log():
    return {"log": log.get_all_messages()}


# GET  Method: Health check
@app.get("/health")
def get_health():
    # Health check might be broken too.
    if config.IS_BROKEN:
        breaker.break_server(config.NAME)
    return {"msg": "OK"}


@app.delete("/log")
def clean_log():
    log.clean()
    return {"log": log.get_all_messages()}


# POST Method: appends a message to the log
@app.post("/log")
def post_log(message, write_concern: int = 1):
    message = Message(message=message)
    logger.info(f"[INFO] [{timeit()}] Server {config.NAME} received message {message}")
    log.append(message)
    if replicator.replicate(message, write_concern=int(write_concern)):
        return {"msg": f"Message added to log, {message}"}
    else:
        return {"msg": f"Message added to log, {message}, but not replicated"}


# POST Method: replicates message on other servers
@app.post("/replicate")
def replicate(message, message_id, timestamp):
    message = Message(message=message, message_id=message_id, timestamp=timestamp)
    logger.info(f"[INFO] [{timeit()}] Server {config.NAME} received message {message}")
    # Simulate malfunction
    if config.IS_BROKEN:
        breaker.break_server(config.NAME)
    log.append(message)
    return {"msg": f"Message added to log, {message}"}


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=int(config.PORT), log_level="debug", access_log=True
    )
