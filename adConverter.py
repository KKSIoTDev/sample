# coding:utf-8
# A/D変換した値を取得する。
#
# 参考サイト
# https://qiita.com/shiraco/items/8c2587ae5a647b4f9803

import RPi.GPIO as GPIO

#####################################################
# A/D変換した値を指定したチャネルから取得する。
# adcnum:チャネル番号(MCP3008の場合、0～7)
# clockpin: SPI_CLKのピン番号
# mosipin : SPI_MOSIのピン番号
# misopin : SPI_MISOのピン番号
# cspin   : チップセレクト(CE〇)のピン番号
#######################################################
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout