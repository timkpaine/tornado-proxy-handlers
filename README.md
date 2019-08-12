# tornado-proxy-handlers
Tornado proxy handlers for HTTP requests and web sockets

[![Build Status](https://travis-ci.org/timkpaine/tornado-proxy-handlers.svg?branch=master)](https://travis-ci.org/timkpaine/tornado-proxy-handlers)
[![Coverage](https://codecov.io/gh/timkpaine/tornado-proxy-handlers/branch/master/graph/badge.svg)](https://codecov.io/gh/timkpaine/tornado-proxy-handlers)

## Overview
This project contains 2 proxy handlers:
- HTTP Handler
- Websocket Handler

The websocket handler requires the http handler for `599` protocol switching. 

## Use
These are designed to be embedded in a tornado server that needs to proxy. They can also be run as a standalone proxy server via the `tornado-proxy` command. 

