# coding:utf-8
# 人体検知モーションセンサー(publisher)
# 人体の動きの検知結果をデータとして送信する。
# ３０秒に１度人体の検知結果をサーバーに送信する。
# 参考サイト
# http://osoyoo.com/2017/03/15/raspberry-pi%E3%81%A7%E4%BA%BA%E4%BD%93%E6%84%9F%E7%9F%A5%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%82%92%E4%BD%9C%E5%8B%95%E3%81%97%E3%80%81led%E3%82%92/
# http://osoyoo.com/ja/2016/07/14/motionsensor-pi/

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
import datetime

#サーバーへの送信間隔
sendInterval = 30

#モーションピンの番号
motion_pin = 17
def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  #モーションセンサーのセットアップ
  GPIO.setup(motion_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

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

# 主処理
# 第一引数：IoT Platformへのアクセスオブジェクト
def main(client):

  #トピック
  topic = "iot-2/evt/eid/fmt/json"

  #前回送信時間
  #初回は必ず実行するために、前回送信日より１年前を指定。
  preSendDateTime = datetime.datetime.now() - datetime.timedelta(weeks=54)

  #送信値（初期値は消灯）
  sendValue = 0

  try:
    while True:
      client.loop() == 0

      #現在時刻
      currentDateTime = datetime.datetime.now()

      #前回送信時間と現在時刻の差分を取る。
      diffDateTime = currentDateTime - preSendDateTime

      #人体感知（モーション）センサーの値を取得
      value=GPIO.input(motion_pin)

      #人体を検知した場合
      if value!=0:

          #点灯するように設定
          sendValue = 1

      #前に送信した時間が３０秒前の場合
      if diffDateTime.total_seconds() > sendInterval:

          #メッセージを設定する
          msg = json.dumps({ "d" : { "sensor" : sendValue } });

          #メッセージをパブリッシュする。
          client.publish(topic,msg, 0, True)

          #人体を感知した場合
          if sendValue!=0:
            print "LED on"
          else:
            print "LED off"

          #前回送信時刻を現在時刻とする。
          preSendDateTime = currentDateTime

          #送信値を消灯にする。
          sendValue = 0

  except KeyboardInterrupt:
      #何も実行しない。
      pass

#初期処理
init()
#IoTPlatformへのアクセス処理
client = connect()
#主処理
main(client)
GPIO.cleanup()