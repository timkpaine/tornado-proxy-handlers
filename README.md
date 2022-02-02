# tornado-proxy-handlers
Tornado proxy handlers for HTTP requests and web sockets

[![Build Status](https://github.com/timkpaine/tornado-proxy-handlers/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/timkpaine/tornado-proxy-handlers/actions?query=workflow%3A%22Build+Status%22)
[![Coverage](https://codecov.io/gh/timkpaine/tornado-proxy-handlers/branch/main/graph/badge.svg)](https://codecov.io/gh/timkpaine/tornado-proxy-handlers)
[![License](https://img.shields.io/github/license/timkpaine/tornado-proxy-handlers.svg)](https://pypi.python.org/pypi/tornado-proxy-handlers/)
[![PyPI](https://img.shields.io/pypi/v/tornado-proxy-handlers.svg)](https://pypi.python.org/pypi/tornado-proxy-handlers/)


## Install
`pip install tornado-proxy-handlers` or from source `python setup.py install`

## Overview
This project contains 2 proxy handlers:
- HTTP Handler
- Websocket Handler

The websocket handler requires the http handler for `599` protocol switching. 

## Use
These are designed to be embedded in a tornado server that needs to proxy. They can also be run as a standalone proxy server via the `tornado-proxy` command. 

