import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from logiled.logi_led import LogitechLed, load_dll


# restore_lighting

load_dll()
print("Initialize...")
logi_led = LogitechLed()

a = logi_led.set_lighting_for_target_zone(1, 100, 0, 0)

input("Press enter to shutdown SDK...")
logi_led.shutdown()
