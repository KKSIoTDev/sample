#!/usr/bin/python
# -*- coding: utf-8 -*-
# 参考URL
#  https://docs.internetofthings.ibmcloud.com/apis/swagger/v0002/info-mgmt.html
#  https://docs.internetofthings.ibmcloud.com/apis/swagger/v0002/http-messaging.html

import requests
import json
import base64
import BluemixAPIConnect

# 指定したデバイスの最新イベントを取得する。
# orgId       ：組織ID
# deviceType  ：デバイスタイプ
# deviceId    ：デバイスID
# eventName   ：イベント名
def getLastEvent(orgId,deviceType,deviceId,eventName):

  #最新イベントを取得するURLを生成
  requestUrl = '/device/types/' + deviceType + '/devices/' + deviceId + '/events/' + eventName

  # BluemixのHTTP APIにアクセスする。
  r = BluemixAPIConnect.accessHttpAPI('GET',orgId,requestUrl)

  # 戻り値をpythonでjson形式に扱えるように変換
  data = json.loads(r.text)

  # base64でエンコードされているので、デコードして戻す。
  return json.loads(data["payload"].decode("base64"))

# 指定したデバイスにメッセージをPublishする。
# orgId       ：組織ID
# deviceType  ：デバイスタイプ
# deviceId a   ：デバイスID
# eventName   ：イベント名
# data        ：データ(JSON形式)
def messagePublish(orgId,deviceType,deviceId,eventName,data):

  #メッセージをパブリッシュするURLを生成
  requestUrl = '/application/types/' + deviceType + '/devices/' + deviceId + '/events/' + eventName

  # BluemixのHTTP APIにアクセスする。
  r = BluemixAPIConnect.accessHttpMessagingAPI(orgId,requestUrl,data)

  return r