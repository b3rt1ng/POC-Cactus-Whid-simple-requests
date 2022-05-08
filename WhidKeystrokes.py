# Cactus Whid HTTP keystrokes POC
# --------------------------------------------------------------
# by B3RT1NG
# https://github.com/b3rt1ng
# --------------------------------------------------------------
# This script is meant to show that it is possible to send
# keystrokes on your Whid devices using the HTTP protocol.
# instead of using the usual Whid Web app.
#
# I'm planning on making a more advanced whid live controller.
# You'll be basically able to cast your keyboard on anyone ;)

import requests

head = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Connection': 'keep-alive',
  'Referer': 'http://192.168.1.1/inputmode',
  'Upgrade-Insecure-Requests': '1',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache'
}

while True:
    requests.post('http://192.168.1.1/runlivepayload', headers = head, data = 'livepayloadpresent=1&livepayload=Print%3A'+input("send: ").replace(' ', '+'))
