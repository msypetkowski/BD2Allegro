#!/bin/bash

function doLibrary {
    autopep8 $1 --in-place
}

function doExecutable {
    doLibrary $1
    chmod +x $1
}

doLibrary ./src/client.py
doLibrary ./src/server.py
doLibrary ./src/clientCore/__init__.py
doLibrary ./src/serverCore/__init__.py
