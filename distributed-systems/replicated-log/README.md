# Replicated Log v01
## Description

Simple echo-client-server app with 2 replication workers and test input generator.

## Usage

Run `docker compose up --build`.

This will start 3 servers: 1 `master` and 2 `secondary`, along with test input client.
Test input will send 10 random messages to the main server, and it will replicate the data along the others.
At the end test app will send GET requests to each server and returns True if all message logs are the same as input one.
-- 

example output of the correct logs
```
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 0: 59"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 1: 16"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 2: 8"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 3: 30"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 4: 71"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 5: 93"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 6: 45"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 7: 24"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 8: 99"}
replicated-log-fake_input-1  | {"msg":"Message added to log, Message 9: 100"}
replicated-log-fake_input-1  | True
```
