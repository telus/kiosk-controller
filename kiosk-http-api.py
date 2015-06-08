#!/usr/bin/env python3

import subprocess, sys
from bottle import route, run, request

def restart():
    subprocess.call("./kiosk start", shell=True)

def getSite():
    file = open('data/kiosk_curr', 'r');
    data = file.read()
    file.close()
    return data

def setSite(newSite, persist=False):
    oldSite = getSite()
    file = open('data/kiosk_page', 'w');
    file.write(newSite);
    file.close();
    restart()
    if not (persist):
        file = open('data/kiosk_page', 'w');
        file.write(oldSite);
        file.close();
    return newSite

@route('/', method='GET')
def status():
    return getSite()

@route('/', method='POST')
def status():
    setSite(request.get_header('kiosk-page', ''))
    return getSite()

@route('/', method='PUT')
def status():
    setSite(request.get_header('kiosk-page', ''), True)
    return getSite()


try:
    port = int(sys.argv[1])
except (ValueError, IndexError):
    port = 8000

run(host='localhost', port=port)
