from pynput import keyboard
from random import randint

from packagename import LogitechLed, load_dll


load_dll()

logi_led = LogitechLed()


def on_press(key):
    r = randint(0, 100)
    g = randint(0, 100)
    b = randint(0, 100)
    logi_led.set_lighting(r, g, b)


def on_release(key):
    if key == keyboard.Key.esc:
        return False


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


logi_led.shutdown()
