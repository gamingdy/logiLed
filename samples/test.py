import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from logipy.logi_led import NotTested, LogitechLed, load_dll


# restore_lighting

load_dll()
print("Initialize...")
logi_led = LogitechLed()

a = logi_led.set_lighting_for_target_zone(1, 100, 0, 0)
print(a)
input("Press enter to shutdown SDK...")
logi_led.shutdown()
# logi_led_test.shutdown()
