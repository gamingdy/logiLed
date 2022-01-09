import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from logipy.logi_led import LogitechLed
import time
import ctypes
import random


print("Initialize...")
logi_led = LogitechLed()
# logi_led.logi_led_pulse_lighting(100, 100, 100, 3000, 500)
# time.sleep(3)
# logi_led.logi_led_set_lighting_for_target_zone(0, 0, 100, 0)
"""
while True:
    time.sleep(0.1)
    zone = random.randint(1, 5)
    red = random.randint(0, 100)
    green = random.randint(0, 100)
    blue = random.randint(0, 100)
    logi_led.logi_led_set_lighting_for_target_zone(zone, red, green, blue)"""

input("Press enter to shutdown SDK...")
logi_led.shutdown()
