#!/bin/sh

waitress-serve --port=5000 --call 'ergate:create_app'