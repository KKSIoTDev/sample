# coding:utf-8
# ボタンを押すと、LED電球が光る。
# 参考サイト
# http://robocad.blog.jp/archives/678444.html
import RPi.GPIO as GPIO
from time import sleep

#ボタンの入力を行うピン番号
button_pin = 16

#LEDの出力を行うピン番号
led_pin = 26

#初期処理
def init():

  global button_pin
  global led_pin

  #GPIOのモードを設定する。
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(led_pin, GPIO.OUT)
  GPIO.setup(button_pin, GPIO.IN)

#主処理
def main():
  global button_pin
  global led_pin
  try:
      while True:
          #ボタンを押下していた場合
          if GPIO.input(button_pin) == GPIO.HIGH:
              #点灯する。
              GPIO.output(led_pin, GPIO.HIGH)
          #ボタンを押下していない場合
          else:
              #消灯する。
              GPIO.output(led_pin, GPIO.LOW)
          sleep(0.01)
  except KeyboardInterrupt:
      pass
#初期処理
init()
#主処理
main()
GPIO.cleanup()