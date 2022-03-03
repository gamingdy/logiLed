import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from logipy.logi_led import NotImplemented, LogitechLed
import time
import ctypes
import random


print("Initialize...")
logi_led = LogitechLed()
b = logi_led.flash_lighting(0, 2**65, 0, 5000, 500)
# logi_led_test = NotImplemented()

# b = logi_led_test.pulse_lighting(0, 100, 0, 5000, 500)
print(b)

input("Press enter to shutdown SDK...")
logi_led.shutdown()
# logi_led_test.shutdown()
