# coding:utf-8
import subprocess
import time
import RPi.GPIO as GPIO
import dht11
import paho.mqtt.client as mqtt

#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# execute
instance = dht11.DHT11(pin=4)

##############################################################################
#####  MQQTプロトコルを利用して、Bluemixにアクセスするための設定を行う。######
##############################################################################

#認証方式
username = "use-token-auth"
#トークンパスワード
password = "4WDIW(38CgtWltpIlI" # 英数字18桁の「認証トークン」を指定します
#組織ID
organization = "ad0utv"     # 6桁の「組織ID」を指定します
#デバイスタイプ
deviceType = "thermostat" # 「デバイス・タイプ」として登録した値を指定します
#デバイスID
deviceSerial = "LivingRoomThermo1" # 「デバイスID」として登録した値を指定します
#トピック
topic = "iot-2/evt/update/fmt/json"
#クライアントＩＤ
clientID = "d:" + organization + ":" + deviceType + ":" + deviceSerial
#ブロッカー
broker = organization + ".messaging.internetofthings.ibmcloud.com"
#ブローカーへの接続先を設定する。
mqttc = mqtt.Client(clientID)

#接続先のユーザとパスワードを設定する。
mqttc.username_pw_set(username, password=password)

#################################
#####  Bluemixに接続する    #####
#################################

try:
    #接続先に接続する。
    mqttc.connect(host=broker, port=1883, keepalive=60)
except Exception as e:
    print "Exception at connect"
    print e

#ネットワークループを開始する。
mqttc.loop_start()

#mqttc.loop()を定期的に実行することによって、接続先との接続を保持する。
while True:
    mqttc.loop()
    result = instance.read()

    #温度センサーからデータを読み取れた場合
    if result.is_valid():
        print("Temp:%d %%" %result.temperature)
        print("Humi:%d %%" %result.humidity)

        #送信する温度および湿度を算出する。
        temp = result.temperature
        humidity = result.humidity

        print "temp = " + str(temp) + ", humidity = " + str(humidity)
        msg = " {\"d\": {\"temp\": " + str(temp) +",\"humidity\": " + str(humidity) + "} }";

        try:
            #送信する温度および湿度をセンサーに送信する。
            mqttc.publish(topic, payload=msg, qos=0, retain=True)
            print "メッセージを送信しました。"
        except Exception as e:
            print "メッセージ送信に失敗しました。"
            print e
        time.sleep(3)

    else:
        print("センサーから温度と湿度を読み取ることができませんでした。")