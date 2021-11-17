#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import time
import hmac
import urllib.parse
import hashlib
import base64
import requests
import json

URL = ""  # 钉钉的webhook
secret = ""  # 钉钉的secret


def get_timestamp_sign():
    global secret
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return (timestamp, sign)


def get_signed_url():
    global URL
    timestamp, sign = get_timestamp_sign()
    webhook = URL + "&timestamp="+timestamp+"&sign="+sign
    return webhook


def send_ding_message(content):
    webhook = get_signed_url()
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    message_json = json.dumps(json.loads(content))
    info = requests.post(url=webhook, data=message_json, headers=header)
    print(info.text)


def main():
    global URL
    global secret
    if len(sys.argv) < 4:
        print("传参错误：webhook  secret content")
        return False
    URL = sys.argv[1]
    secret = sys.argv[2]
    content = sys.argv[3]
    send_ding_message(content)


if __name__ == "__main__":
    main()
