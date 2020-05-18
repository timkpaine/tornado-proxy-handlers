# tornado-proxy-handlers
Tornado proxy handlers for HTTP requests and web sockets

[![Build Status](https://dev.azure.com/tpaine154/miscellaneous/_apis/build/status/timkpaine.tornado-proxy-handlers?branchName=master)](https://dev.azure.com/tpaine154/miscellaneous/_build/latest?definitionId=29&branchName=master)
[![Coverage](https://img.shields.io/azure-devops/coverage/tpaine154/miscellaneous/29/master)](https://img.shields.io/azure-devops/coverage/tpaine154/miscellaneous/29)
[![License](https://img.shields.io/github/license/timkpaine/tornado-proxy-handlers.svg)](https://pypi.python.org/pypi/tornado-proxy-handlers/)
[![PyPI](https://img.shields.io/pypi/v/tornado-proxy-handlers.svg)](https://pypi.python.org/pypi/tornado-proxy-handlers/)
[![Docs](https://readthedocs.org/projects/tornado-proxy-handlers/badge/?version=latest)](https://tornado-proxy-handlers.readthedocs.io/en/latest/?badge=latest)


## Install
`pip install tornado-proxy-handlers` or from source `python setup.py install`

## Overview
This project contains 2 proxy handlers:
- HTTP Handler
- Websocket Handler

The websocket handler requires the http handler for `599` protocol switching. 

## Use
These are designed to be embedded in a tornado server that needs to proxy. They can also be run as a standalone proxy server via the `tornado-proxy` command. 

