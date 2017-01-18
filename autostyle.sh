#!/bin/bash

function doLibrary {
    autopep8 $1 --in-place -r
}

function doExecutable {
    doLibrary $1
    chmod +x $1
}

doLibrary Shop
doLibrary ShopApp
doExecutable manage.py
