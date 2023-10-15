# Your App Name

## Description

A brief description of your app.

## Installation

Instructions on how to install your app.

## Usage

Run `docker compose up --build`

This will start 3 servers: 1 `master` and 2 `secondary`, along with test input client.
Test input will send 10 random messages to the main server, and it will replicate the data along the others.
At the end test app will send GET requests to each server and returns True if all message logs are the same as input one.
