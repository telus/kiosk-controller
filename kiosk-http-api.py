#!/usr/bin/env python3

import subprocess, sys
from bottle import route, run, request, response

kiosk_script = sys.argv[1]
server_port = int(sys.argv[2])
current_page_file = sys.argv[3]
saved_page_file = sys.argv[4]
temp_page_file = sys.argv[5]

def restartChromium():
    subprocess.call(kiosk_script + " chromium", shell=True)

def readFile(fileName):
    file = open(fileName, 'r');
    data = file.read()
    file.close()
    return data

def overwriteFile(data, filename):
    file = open(filename, 'w');
    file.write(data);
    file.close();

def getPage():
    response.content_type = "text/plain"
    return readFile(current_page_file)

def setTempPage(url):
    overwriteFile(url, temp_page_file)

def setPage(url):
    overwriteFile(url, saved_page_file)

@route('/', method='GET')
def status():
    return getPage()

@route('/', method='POST')
def status():
    newpage = request.get_header('kiosk-page', '')
    if len(newpage) > 0:
        setTempPage(newpage)
    restartChromium()
    return getPage()

@route('/', method='PUT')
def status():
    newpage = request.get_header('kiosk-page', '')
    if len(newpage) > 0:
        setPage(newpage)
        restartChromium()
        return getPage()
    response.status = "400 No page specified"

run(host='localhost', port=server_port)
