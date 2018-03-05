#!/usr/bin/python
# -*- coding: utf-8 -*-
# 人体検知センサー(subscriber)
# センサー情報を受取、センサーが人体を感知していた場合は、LEDライトを点灯する。
# subscriberは常に待ち受け状態とし、publisherからのメッセージ受信をトリガーにして動作する。
# 参考サイト
# http://osoyoo.com/2017/03/15/raspberry-pi%E3%81%A7%E4%BA%BA%E4%BD%93%E6%84%9F%E7%9F%A5%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%82%92%E4%BD%9C%E5%8B%95%E3%81%97%E3%80%81led%E3%82%92/
# https://qiita.com/f_nishio/items/0b5161207a110f7bbef4
# https://qiita.com/egplnt/items/552b91210be5d03430b4

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
import RPi.GPIO as GPIO


#LEDのピン番号
led_pin = 26

def init():
  global led_pin
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  #GPIOのPIN番号を指定する。
  GPIO.setup(led_pin,GPIO.OUT)

#コネクション接続時のコールバック関数
def on_connect(client, userdata, flags, rc):
    #subscribeする。
    client.subscribe("iot-2/type/motion/id/motion/evt/eid/fmt/json")

#subscribe時のコールバック関数
def on_message(client, userdata, msg):
    global led_pin

    #センサーからのJSONデータを取得
    data = json.loads(msg.payload)

    #センサーの値を取得
    value = data["d"]["sensor"]

    #センサーの情報がONの場合
    if value == 1:
        #LEDを点灯する。
        GPIO.output(led_pin,GPIO.HIGH)
        print "LEDを点灯します"
    else:
        #LEDを消灯する。
        GPIO.output(led_pin,GPIO.LOW)
        print "LEDを消灯します"

# IoT Platformに接続する。
def connect():

  #組織ID
  organization = "ad0utv"

  #クライアント固有のアプリケーションID
  applId = "motionSample"

  #APIキー
  username = "a-ad0utv-9vndccqqop" #APIキーを指定します。

  #APIトークンパスワード
  password = "I9ZNa)eq8ZFNKZ7JAv"  # 英数字18桁の「認証トークン」を指定します

  #クライアントID（クライアントタイプ・アプリケーション）
  clientID = "a:" + organization + ":" + applId

  #ブローカー
  broker = organization + ".messaging.internetofthings.ibmcloud.com"

  mqttc = mqtt.Client(clientID)
  mqttc.username_pw_set(username, password=password)

  #コネクション接続時のコールバック関数を指定
  mqttc.on_connect = on_connect

  #メッセージ受信時のコールバック関数を指定
  mqttc.on_message = on_message

  #接続
  mqttc.connect(host=broker, port=1883, keepalive=60)

  return mqttc

#主処理
#第一引数：IoT Platformとの接続オブジェクト
def main(client):
  try:
    #待ち受け状態にする。
    client.loop_forever()
  except KeyboardInterrupt:
      #何も実行しない。
      pass

#初期処理
init()
#IoT Platformに接続する。
client = connect()
#主処理
main(client)
GPIO.cleanup()