# coding:utf-8
# 椅子に座った時の圧力で、在席状況を把握する。
# ５秒に１度データを送信し、閾値を超えた値があれば在席していた旨の情報を送信する。
#
# 参考サイト
# https://qiita.com/shiraco/items/8c2587ae5a647b4f9803
# http://kousen-tech.blogspot.jp/2016/10/raspberry-pi_30.html
#

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
import datetime
import adConverter

#圧力センサーで人がいると判断する条件
threshold = 500

#サーバーへの送信間隔（秒）
sendInterval = 5

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

# IoT Platformへの接続を確立
# 戻り値：IoT Platformへのアクセスオブジェクト
def connect():
  #組織ID
  organization = "ad0utv"     # 6桁の「組織ID」を指定します

  #デバイスタイプ
  deviceType = "motion" # 「デバイス・タイプ」として登録した値を指定します

  #デバイスID
  deviceSerial = "motion" # 「デバイスID」として登録した値を指定します

  #認証方式
  username = "use-token-auth"

  #トークンパスワード
  password = "-xNZuj8ecZbrv*dFo_" # 英数字18桁の「認証トークン」を指定します

  #ブローカー
  broker = organization + ".messaging.internetofthings.ibmcloud.com"

  #クライアントＩＤ
  clientID = "d:" + organization + ":" + deviceType + ":" + deviceSerial

  #クライアントへの接続
  client = mqtt.Client(clientID)

  #ユーザとパスワードをセット
  client.username_pw_set(username, password)

  #接続
  client.connect(broker, port=1883, keepalive=60)

  return client

#主処理
def main(client):
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

  #トピック
  topic = "iot-2/evt/eid/fmt/json"
  try:

    while True:
      #１秒毎に計測する。
      time.sleep(1)

      #サーバーとの接続を確立し続けるために、実施する。
      client.loop()

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
      if diffDateTime.total_seconds() > sendInterval:

        #メッセージを設定する
        msg = json.dumps({ "d" : { "sensor" : sendValue } });

        #メッセージをパブリッシュする。
        client.publish(topic,msg, 0, True)

        #前回送信時刻を現在時刻とする。
        preSendDateTime = currentDateTime

        #送信値を消灯にする。
        sendValue = 0
  except:
      import traceback
      traceback.print_exc()

# 初期処理
init()
# IoT PlatFormへの接続処理
client = connect()
# 主処理
main(client)
#GPIO.cleanup()