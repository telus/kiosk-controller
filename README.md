Kiosk Controller
================

A CLI app and HTTP API to remotely control Chromium running in a kiosk mode.

Originally built for opening dashboards on TV-connected Raspberry Pis.

**NOTE**: Since Chrome/Chromium is multi-process, the author was unable to find a reliable way to target a single window/tab. Instead, `kiosk` terminates all chromium processes before creating a new one when (re)starting.

## Dependencies

Kiosk Controller requires: `chromium-browser` and `python3`. Running any `./kiosk` command will let you know if they are missing.

## CLI

Run `./kiosk help` for a list of available commands.

## HTTP API

By default, kiosk will start an HTTP API. A HTTP header of 'kiosk-auth' will be needed if you set an API password using the CLI.

**`GET / ` - Current status**

Returns the plain text of the currently set page.

**`POST /` - Temporarily change page**

If a HTTP header `kiosk-page` is specified, the page will be temporarily changed and Chromium will restart.

Otherwise, the browser will restart with the default page.

**`PUT / ` - Permanently change page**

If a HTTP header `kiosk-page` is specified, the page will be saved as the new default and Chromium will restart.

Otherwise, if no page is specified, an HTTP 400 is returned.

##Todo

- Code review

#Ideas

- An iframe + sockets based page could get around the chromium control issues. The CLI could hook into a server sending messages to the client to switch the page, reload it, etc.
