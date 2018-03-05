# coding:utf-8
# 椅子に座った時の圧力で、在席状況を把握する。
# ５秒に１度データを送信し、閾値を超えた値があれば在席していた旨の情報を送信する。
#
# 参考サイト
# http://iinpht.jeez.jp/raspberrypi/raspberry-pi%E3%81%A7%E5%9C%A7%E5%8A%9B%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E3%82%92%E4%BD%BF%E3%81%86
# http://kousen-tech.blogspot.jp/2016/10/raspberry-pi_30.html
#

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
import datetime
import spidev

#圧力センサーで人がいると判断する条件
threshold = 40

#サーバーへの送信間隔（秒）
sendInterval = 5

#初期処理
def init():
  #SPIデバイス
  spi = spidev.SpiDev()

  #SPIデバイスオープン
  spi.open(0, 0)

  return spi

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
def main(client,spi):
  global threshold

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

      #チャネル0の信号を取得する。
      resp = spi.xfer2([0x68, 0x00])

      #チャネル0から値を取得する。
      value = (resp[0] * 256 + resp[1]) & 0x3ff

      #現在時刻
      currentDateTime = datetime.datetime.now()

      #前回送信時間と現在時刻の差分を取る。
      diffDateTime = currentDateTime - preSendDateTime

      print value

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
  except KeyboardInterrupt:
      #何も実行しない。
      pass

# 初期処理
spi = init()
# IoT PlatFormへの接続処理
client = connect()
# 主処理
main(client,spi)
GPIO.cleanup()