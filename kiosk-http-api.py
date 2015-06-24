#!/usr/bin/env python3

import subprocess, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

kiosk_script, server_port, current_page_file, \
saved_page_file, temp_page_file = sys.argv[1:6]
try:
    server_auth = sys.argv[6]
except IndexError:
    server_auth = ""

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
    return readFile(current_page_file)

def setTempPage(url):
    overwriteFile(url, temp_page_file)

def setPage(url):
    overwriteFile(url, saved_page_file)

class KioskHandler(BaseHTTPRequestHandler):
    def handle(self):
        '''Overridden from parent to perform authorization'''
        self.raw_requestline = self.rfile.readline()
        if not self.parse_request():
            return
        if server_auth != self.headers.get('kiosk-auth', ''):
            self.send_error(401)
            return
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(405)
            return
        method = getattr(self, mname)
        method()

    def sendPlainText(self, message):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(message.strip(), 'utf-8'))

    def do_GET(self):
        self.sendPlainText(getPage())

    def do_POST(self):
        newpage = self.headers.get('kiosk-page', '')
        if len(newpage) > 0:
            setTempPage(newpage)
        restartChromium()
        self.sendPlainText(getPage())

    def do_PUT(self):
        newpage = self.headers.get('kiosk-page', '')
        if len(newpage) > 0:
            setPage(newpage)
            restartChromium()
            self.sendPlainText(getPage())
            return
        self.send_error(400)

httpd = HTTPServer(('localhost', int(server_port)), KioskHandler)
httpd.serve_forever()
