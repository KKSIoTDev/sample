#!/usr/bin/python
# -*- coding: utf-8 -*-

#参考サイト
#https://qiita.com/egplnt/items/e9af5d5abeab08f5a455

import logging
import os
import os.path
import sys
import codecs
import time
import paho.mqtt.client as mqtt
import json
import threading
import random

broker = ""
i = 0

#認証方式
username = "use-token-auth"

#組織ID
organization = "hn7pp2"     # 6桁の「組織ID」を指定します

#デバイスタイプ
deviceType = "temperature" # 「デバイス・タイプ」として登録した値を指定します

#デバイスID
deviceSerial = "temperature" # 「デバイスID」として登録した値を指定します

#トークンパスワード
password = "i?1t2KZ&&L-Dyls1Xc" # 英数字18桁の「認証トークン」を指定します

#トピック
topic = "iot-2/evt/update/fmt/json"

#クライアントＩＤ
clientID = "d:" + organization + ":" + deviceType + ":" + deviceSerial

#ブロッカー
broker = organization + ".messaging.internetofthings.ibmcloud.com"

#ブローカーへの接続先を設定する。
mqttc = mqtt.Client(clientID)

if username is not "":
    #接続先のユーザとパスワードを設定する。
    mqttc.username_pw_set(username, password=password)

    try:
        #接続する。
        mqttc.connect(host=broker, port=1883, keepalive=60)
    except Exception as e:
        print "Exception at connect"
        print e

#ネットワークループを開始する。
mqttc.loop_start()

#mqttc.loop()を定期的に実行することによって、接続先との接続を保持する。
while mqttc.loop() == 0:

    #送信する温度および湿度を算出する。
    temp = random.randrange(-10,40)
    humidity = random.randrange(20,99)
    print "temp = " + str(temp) + ", humidity = " + str(humidity)
    msg = " {\"d\": {\"temp\": " + str(temp) +",\"humidity\": " + str(humidity) + "} }";

    try:
        #送信する温度および湿度をセンサーに送信する。
        mqttc.publish(topic, payload=msg, qos=0, retain=True)
        print "message published"
        # print raw_input("[Enter] to send another request")
    except Exception as e:
        print "Exception at publish"
        print e

    time.sleep(10)
    #ループ回数が１０回を超えると、ループを抜ける。
    if i > 10:
      break

    i = i +1
    pass
