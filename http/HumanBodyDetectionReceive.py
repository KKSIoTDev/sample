#!/usr/bin/python
# -*- coding: utf-8 -*-
# センサー情報を受取、センサーが人体を感知していた場合は、LEDライトを点灯する。
# 設定した間隔毎にデータを取得する。HTTPプロトコルを利用して通信する。

import time
import json
import RPi.GPIO as GPIO
import datetime
import BluemixAPIUse

#LEDのピン番号
led_pin = 26
#データ取得の間隔
interval = 1

def init():
  global led_pin
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  #GPIOのPIN番号を指定する。
  GPIO.setup(led_pin,GPIO.OUT)

#主処理
#第一引数：IoT Platformとの接続オブジェクト
def main():

  global interval
  global led_pin

  #前回取得時間
  #初回は必ず実行するために、前回送信日より１年前を指定。
  preGetDateTime = datetime.datetime.now() - datetime.timedelta(weeks=54)

  try:

    while True:

      #現在時刻
      currentDateTime = datetime.datetime.now()

      #前回の取得時間と現在時刻の差分を取る。
      diffDateTime = currentDateTime - preGetDateTime

      #前にサーバーに取得した時間が設定した時間を超えた場合
      if diffDateTime.total_seconds() > interval:

        #メッセージを取得する。
        data = BluemixAPIUse.getLastEvent('ad0utv','motion','motion','eid')

        #データをJSON形式に変換
        data = json.loads(data)

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

        #前回送信時刻を現在時刻とする。
        preGetDateTime = currentDateTime

        #送信値を消灯にする。
        sendValue = 0

  except:
      import traceback
      traceback.print_exc()

#初期処理
init()
#主処理
main()
GPIO.cleanup()