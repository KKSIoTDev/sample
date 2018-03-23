#!/usr/bin/python
# -*- coding: utf-8 -*-
# 参考URL
#  https://console.bluemix.net/docs/services/IoT/reference/api.html#api_overview
#  https://www.ibm.com/support/knowledgecenter/ja/SSFKSJ_9.0.0/com.ibm.mq.sec.doc/q128710_.htm

import requests
import base64

#APIキー
username = 'a-ad0utv-9vndccqqop'
#APIトークンパスワード
password = 'I9ZNa)eq8ZFNKZ7JAv'
#API認証
auth ="Basic " + (username + ':' + password).encode("base64")[:-1]
#APIの認証ヘッダ
head = {'Authorization':auth,'Content-type': 'application/json'}

# BluemixのREST APIにアクセスする。
# method ：HTTPメソッド     POST,GET,PUT,DELETE
# orgId  ：組織コード
# url    ：APIのURL
# param  ：パラメータ       省略時 None
# data   ：データ(JSON形式) 省略時 None
def accessHttpAPI(method,orgId,url,param = None,data = None):
  global head

  print head
  requestUrl = 'https://'+orgId+'.internetofthings.ibmcloud.com/api/v0002'+url
  print requestUrl
  r = requests.request(method,requestUrl,params=param,headers=head,json=data)

  #異常終了した場合
  if r.status_code >= 300 and  r.status_code < 400:

    print "ステータスコード：" + str(r.status_code)

  elif r.status_code >= 400 :

    print "異常終了しました。"
    print "ステータスコード：" + str(r.status_code)

  return r

# BluemixのHTTP Messaging APIにアクセスする。
# orgId  ：組織コード
# url    ：APIのURL
# data   ：データ(JSON形式) 省略時 None
def accessHttpMessagingAPI(orgId,url,data = None):

  global head

  requestUrl = 'https://'+orgId+'.messaging.internetofthings.ibmcloud.com:443/api/v0002' + url

  r = requests.request('POST',requestUrl,json=data,headers=head)

  #異常終了した場合
  if r.status_code >= 300 and  r.status_code < 400:

    print "ステータスコード：" + str(r.status_code)

  elif r.status_code >= 400 :

    print "異常終了しました。"
    print "ステータスコード：" + str(r.status_code)

  return r