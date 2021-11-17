# -*-coding:utf-8-*-
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

URL = "https://oapi.dingtalk.com/robot/send?access_token=f927e70f5fdbc0cb3e529e59f65c7772cdec0beb5aa52bd2a42fd90fe8b910e1"


def get_timestamp_sign():
    timestamp = str(round(time.time() * 1000))
    secret = "SEC9ef228a12d4fc2c6e9b2d42cc24c7a0e27350b505477cc0dd045059dda65e07f"  # SEC开头的
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print("timestamp: ", timestamp)
    print("sign:", sign)
    return (timestamp, sign)


def get_signed_url():
    timestamp, sign = get_timestamp_sign()
    webhook = URL + "&timestamp="+timestamp+"&sign="+sign
    return webhook


def get_webhook(mode):

    if mode == 0:  # only 敏感字
        webhook = URL
    elif mode == 1 or mode == 2:  # 敏感字和加签 或 # 敏感字+加签+ip
        # 加签： https://oapi.dingtalk.com/robot/send?access_token=XXXXXX&timestamp=XXX&sign=XXX
        webhook = get_signed_url()
    else:
        webhook = ""
        print("error! mode:   ", mode, "  webhook :  ", webhook)
    return webhook


def get_message(content, is_send_all):
    # 和类型相对应，具体可以看文档 ：https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    # 可以设置某个人的手机号，指定对象发送
    message = {
        "msgtype": "text",  # 有text, "markdown"、link、整体跳转ActionCard 、独立跳转ActionCard、FeedCard类型等
        "text": {
            "content": content  # 消息内容
        },
        "at": {
            "atMobiles": [
                "1862*8*****6",
            ],
            "isAtAll": is_send_all  # 是否是发送群中全体成员
        }
    }

    message = {
        "msgtype": "link",
        "link": {
            "text": "这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林",
            "title": "时代的火车向前开",
            "picUrl": "",
            "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
        }
    }

    message = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": "我 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
            "text": "![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png) \n\n #### 乔布斯 20 年前想打造的苹果咖啡厅 \n\n Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
            "btnOrientation": "1",
            "btns": [
                {
                    "title": "内容不错",
                    "actionURL": "https://www.dingtalk.com/"
                },
                {
                    "title": "不感兴趣",
                    "actionURL": "https://www.dingtalk.com/"
                }
            ]
        }
    }

    print(message)
    return message


def send_ding_message(content, is_send_all):
    # 请求的URL，WebHook地址
    webhook = get_webhook(1)  # 主要模式有 0 ： 敏感字 1：# 敏感字 +加签 3：敏感字+加签+IP
    print("webhook: ", webhook)
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    # 构建请求数据
    message = get_message(content, is_send_all)
    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=webhook, data=message_json, headers=header)
    # 打印返回的结果
    print(info.text)


if __name__ == "__main__":
    content = "test,机器人测试,hello！"
    is_send_all = False
    send_ding_message(content, is_send_all)
