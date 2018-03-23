# coding:utf-8
# 椅子に座った時の圧力で、在席状況を把握する。
# ５秒に１度データを送信し、閾値を超えた値があれば在席していた旨の情報を送信する。
# 通信はHTTPプロトコルを使用する。

import RPi.GPIO as GPIO
import time
import json
import datetime
import adConverter
import BluemixAPIUse


#圧力センサーで人がいると判断する条件
threshold = 1200

#サーバーへの送信間隔（秒）
interval = 1

# SPI通信するためのピン番号
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

#初期処理
def init():

  # GPIOのピン番号を指定するモードの指定
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  # SPI通信するためのピン番号を設定
  GPIO.setup(SPIMOSI, GPIO.OUT)
  GPIO.setup(SPIMISO, GPIO.IN)
  GPIO.setup(SPICLK, GPIO.OUT)
  GPIO.setup(SPICS, GPIO.OUT)

#主処理
def main():
  global threshold
  global SPICLK
  global SPIMOSI
  global SPIMISO
  global SPICS

  #前回送信時間
  #初回は必ず実行するために、前回送信日より１年前を指定。
  preSendDateTime = datetime.datetime.now() - datetime.timedelta(weeks=54)

  #送信値（初期値は消灯）
  sendValue = 0

  try:

    while True:

      #A/D変換した結果を取得する。
      value = adConverter.readadc(0, SPICLK, SPIMOSI,SPIMISO, SPICS)

      print value

      #現在時刻
      currentDateTime = datetime.datetime.now()

      #前回送信時間と現在時刻の差分を取る。
      diffDateTime = currentDateTime - preSendDateTime

      #重さが閾値以上の場合
      if value >= threshold:
        sendValue = 1

      #前にサーバーに送信した時間が設定した時間を超えた場合
      if diffDateTime.total_seconds() > interval:

        #メッセージを設定する
        msg = json.dumps({ "d" : { "sensor" : sendValue } });

        #メッセージをパブリッシュする。
        BluemixAPIUse.messagePublish('ad0utv','motion','motion','eid',msg)

        #前回送信時刻を現在時刻とする。
        preSendDateTime = currentDateTime

        #送信値を消灯にする。
        sendValue = 0
  except:
      import traceback
      traceback.print_exc()

# 初期処理
init()
# 主処理
main()