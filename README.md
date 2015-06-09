Kiosk Controller
================

A CLI app and HTTP API to remotely control Chromium running in a kiosk mode.

Originally built for opening dashboards on TV-connected Raspberry Pis.

## Usage

Kiosk Controller requires:

- `chromium-browser`
- `python3`
- `bottle.py` library

Running `./kiosk` will notify you of missing dependencies and how to fix them.

Otherwise, it will display usage help.

## HTTP API

By default, kiosk will start an HTTP API with the following endpoints:

**`GET / ` - Current status** 

Returns the plain text of the currently set page.

**`POST /` - Temporarily change page**

If a HTTP header `kiosk-page` is specified, the page will be temporarily changed and Chromium will restart.

Otherwise, the browser will restart with the default page.

**`PUT / ` - Permanently change page**

If a HTTP header `kiosk-page` is specified, the page will be saved as the new default and Chromium will restart.

Otherwise, if no page is specified, an HTTP 400 is returned.

##Todo

- fix chrome restart failing to close old window
- Add API auth
- Code review
- Remove dependency on bottle?
