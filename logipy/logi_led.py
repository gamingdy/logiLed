"""
.. note::
    logi_led.py : Defines the exported functions for the API Logitech Gaming LED SDK \n
    Original author: **Tom Lambert**

    This is a fork of https://github.com/Logitech/logiPy by **gamingdy**
"""

import ctypes
import os
import struct
from pathlib import Path


class SDKNotFoundException(BaseException):
    """
    Raised if the SDK DLL file cannot be found.
    """

    pass


class LGHUBNotLaunched(BaseException):
    """
    Raised if Logitech G Hub is not launched
    """

    pass


class RangeError(BaseException):
    """
    Raised if given value is in incorrect range
    """

    pass


class ConnectionLost(BaseException):
    pass


# Helpers
#
class Color:
    # an RGBA color object that can be created using RGB, RGBA, color name, or a hex_code.

    def __init__(self, *args, **kwargs):
        red, green, blue, alpha = 0, 0, 0, 255
        hex_code = None
        if len(args) > 0:
            if isinstance(args[0], int):
                red, green, blue = args[0], args[1], args[2]
                if len(args) > 3:
                    alpha = args[3]
            elif isinstance(args[0], str):
                if len(args) > 1:
                    alpha = args[1]
                if args[0] == "red":
                    red, green, blue = 255, 0, 0
                elif args[0] == "orange":
                    red, green, blue = 255, 165, 0
                elif args[0] == "yellow":
                    red, green, blue = 255, 255, 0
                elif args[0] == "green":
                    red, green, blue = 0, 255, 0
                elif args[0] == "blue":
                    red, green, blue = 0, 0, 255
                elif args[0] == "indigo":
                    red, green, blue = 75, 0, 130
                elif args[0] == "violet":
                    red, green, blue = 238, 130, 238
                elif args[0] == "cyan":
                    red, green, blue = 0, 220, 255
                elif args[0] == "pink":
                    red, green, blue = 255, 0, 255
                elif args[0] == "purple":
                    red, green, blue = 128, 0, 255
                elif args[0] == "white":
                    red, green, blue = 255, 255, 255
                elif args[0] == "black":
                    red, green, blue = 0, 0, 0
                else:
                    hex_code = args[0]
                    hex_code = kwargs.pop("hex", hex_code)
        if hex_code:
            hex_code = hex_code.replace("#", "")
            self.red, self.green, self.blue = struct.unpack(
                "BBB", hex_code.decode("hex")
            )
            self.alpha = alpha
        elif any(x in ["red", "blue", "green", "alpha"] for x in kwargs):
            self.red = kwargs.pop("red", red)
            self.green = kwargs.pop("green", green)
            self.blue = kwargs.pop("blue", blue)
            self.alpha = kwargs.pop("alpha", alpha)
        else:
            self.red = red
            self.green = green
            self.blue = blue
            self.alpha = alpha
        self.hex_code = "#{h}".format(
            h=struct.pack("BBB", *(self.red, self.green, self.blue)).encode("hex")
        )

    def rgb_percent(self):
        return (
            int((self.red / 255.0) * 100),
            int((self.green / 255.0) * 100),
            int((self.blue / 255.0) * 100),
        )


def check_maximum(values, maximum):
    for value in values:
        if value > maximum:
            raise RangeError(f"Value can't be greater than {maximum}")
    return True


def check_negative(values):
    for value in values:
        if value < 0:
            raise RangeError("Value can't be negative")
    return True


def execute(funct, *args):
    result = funct(*args)
    if result:
        return True

    raise ConnectionLost(
        f"Connection with Logitech SDK is lost, try to restart LogitechGHub"
    )


class LogitechLed:
    """
    .. note::
        The following class is the main class of library
    """

    def __init__(self):
        self.led_dll = led_dll

    def shutdown(self):
        """
        Restores the last saved lighting and frees memory used by the SDK.
        """
        return execute(self.led_dll.LogiLedShutdown)

    def save_current_lighting(self):
        """
        Saves the current lighting so that it can be restored after a temporary effect is finished.

        .. note::
            On per-key backlighting supporting devices, this function will save the current state for each key.
        """
        return execute(self.led_dll.LogiLedSaveCurrentLighting)

    def set_lighting(self, red_percentage, green_percentage, blue_percentage):
        """
        Sets the lighting on connected and supported devices.

        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct

        """
        check_negative((red_percentage, green_percentage, blue_percentage))
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)

        return execute(
            self.led_dll.LogiLedSetLighting,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def flash_lighting(
        self,
        red_percentage,
        green_percentage,
        blue_percentage,
        ms_duration,
        ms_interval,
    ):
        """
        Plays the flashing effect on the targeted devices by combining the RGB percentages, for a defined duration in
        milliseconds with a given interval.

        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.
        :param int ms_duration: Duration of effect in millisecond.
        :param int ms_interval: Interval duration between each effect in millisecond.

        :raises RangeError: Raised if color percentage range is not correct

        .. tip::
            Specifying a **ms_duration** to 0 will cause the effect to be infinite until reset
        """
        check_negative(
            (
                red_percentage,
                green_percentage,
                blue_percentage,
                ms_duration,
                ms_interval,
            )
        )
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)
        return execute(
            self.led_dll.LogiLedFlashLighting,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )

    def pulse_lighting(
        self,
        red_percentage,
        green_percentage,
        blue_percentage,
        ms_duration,
        ms_interval,
    ):
        """
        Pulses the lighting color of the combined RGB percentages, for a defined duration in milliseconds with a given
        interval.

        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.
        :param int ms_duration: Duration of effect in millisecond.
        :param int ms_interval: Interval duration between each effect in millisecond.

        :raises RangeError: Raised if color percentage range is not correct

        .. tip::
            Specifying a **ms_duration** to 0 will cause the effect to be infinite until reset
        """
        check_negative(
            (
                red_percentage,
                green_percentage,
                blue_percentage,
                ms_duration,
                ms_interval,
            )
        )
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)
        return execute(
            self.led_dll.LogiLedPulseLighting,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )

    def stop_effects(self):
        """Stops any of the presets effects (started from :func:`flash_lighting` or :func:`pulse_lighting`)."""
        return execute(self.led_dll.LogiLedStopEffects)

    def set_lighting_for_target_zone(
        self,
        zone,
        red_percentage,
        green_percentage,
        blue_percentage,
    ):
        """
        Sets lighting on a specific zone for all connected zonal devices that match the device type

        :param int zone: Zone id on target device
        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct

        """
        check_negative((zone, red_percentage, green_percentage, blue_percentage))
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)
        return execute(
            self.led_dll.LogiLedSetLightingForTargetZone,
            None,
            zone,
            red_percentage,
            green_percentage,
            blue_percentage,
        )


class NotTested:
    """
    .. warning::
        A list of untested functions, which can be used but for which we are not sure of the correct operation.
    """

    def __init__(self):
        self.led_dll = led_dll

    def flash_single_key(
        self,
        key_name,
        red_percentage,
        green_percentage,
        blue_percentage,
        ms_duration,
        ms_interval,
    ):
        """
        Plays the flashing effect on the key passed as parameter, by combining the RGB percentages, for a defined
        duration in milliseconds with a given interval.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_name: The key to restore the color on.
        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.
        :param int ms_duration: Duration of effect in millisecond.
        :param int ms_interval: Interval duration between each effect in millisecond.

        :raises RangeError: Raised if color percentage range is not correct

        .. tip::
            Specifying a **ms_duration** to 0 will cause the effect to be infinite until reset
        """
        check_negative(
            (
                red_percentage,
                green_percentage,
                blue_percentage,
                ms_duration,
                ms_interval,
            )
        )
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)
        return execute(
            self.led_dll.LogiLedFlashSingleKey,
            key_name,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )

    def pulse_single_key(
        self,
        key_name,
        red_percentage_start,
        green_percentage_start,
        blue_percentage_start,
        ms_duration,
        is_infinite=False,
        red_percentage_end=0,
        green_percentage_end=0,
        blue_percentage_end=0,
    ):
        """
        Starts a pulsing effect on the key passed as parameter.
        The key will be pulsing with from start color to finish color for msDuration milliseconds.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_name: The key to restore the color on.
        :param int red_percentage_start: Amount of red in the start color of the effect. **Range is 0 to 100**.
        :param int green_percentage_start: Amount of green in the start color of the effect. **Range is 0 to 100**.
        :param int blue_percentage_start: Amount of blue in the start color of the effect. **Range is 0 to 100**.
        :param int ms_duration: Duration of effect in millisecond.
        :param bool is_infinite: If set to True, it will loop infinitely until stopped with a called to :func:`stop_effects_on_key` or :func:`stop_effects <LogitechLed.stop_effects>`
        :param int red_percentage_end: Amount of red in the finish color of the effect. **Range is 0 to 100**.
        :param int green_percentage_end: Amount of green in the finish color of the effect. **Range is 0 to 100**.
        :param int blue_percentage_end: Amount of blue in the finish color of the effect. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct

        """
        check_negative(
            (
                red_percentage_start,
                green_percentage_start,
                blue_percentage_start,
                red_percentage_end,
                green_percentage_end,
                blue_percentage_end,
                ms_duration,
            )
        )
        check_maximum(
            (
                red_percentage_start,
                green_percentage_start,
                blue_percentage_start,
                red_percentage_end,
                green_percentage_end,
                blue_percentage_end,
            ),
            100,
        )
        return execute(
            self.led_dll.LogiLedPulseSingleKey,
            key_name,
            red_percentage_start,
            green_percentage_start,
            blue_percentage_start,
            red_percentage_end,
            green_percentage_end,
            blue_percentage_end,
            ms_duration,
            is_infinite,
        )

    def restore_lighting(self):
        """
        Restores the last saved lighting. It should be called after a temporary effect is finished.

        .. note::
            On per-key backlighting supporting devices, this function will restore the saved state for each key
        """
        return execute(self.led_dll.LogiLedRestoreLighting)

    def restore_lighting_for_key(self, key_name):
        """
        Restores the saved color on the key passed as argument.
        Use this function with the :func:`save_lighting_for_key` to preserve
        the state of a key before applying any effect.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_name: The key to restore the color on.
        """
        return execute(self.led_dll.LogiLedRestoreLightingForKey, key_name)

    def save_lighting_for_key(self, key_name):
        """
        Saves the current color on the keycode passed as argument.
        Use this function with the :func:`restore_lighting_for_key`
        to preserve the state of a key before applying any effect.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_name: The key to save the color for.

        """
        return execute(self.led_dll.LogiLedSaveLightingForKey, key_name)

    def set_lighting_for_key_with_hid_code(
        self, key_code, red_percentage, green_percentage, blue_percentage
    ):
        """
        Sets the key identified by the hid code passed as parameter to the desired color.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_code: The hid-code of the key to set
        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct
        """
        check_negative((red_percentage, green_percentage, blue_percentage))
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)

        return execute(
            self.led_dll.LogiLedSetLightingForKeyWithHidCode,
            key_code,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_for_key_with_key_name(
        self, key_name, red_percentage, green_percentage, blue_percentage
    ):
        """
        Sets the key identified by the code passed as parameter to the desired color.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_name: The name of the key to set
        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct
        """
        check_negative((red_percentage, green_percentage, blue_percentage))
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)

        return execute(
            self.led_dll.LogiLedSetLightingForKeyWithKeyName,
            key_name,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_for_key_with_quartz_code(
        self, key_code, red_percentage, green_percentage, blue_percentage
    ):
        """
        Sets the key identified by the quartz code passed as parameter to the desired color

        .. warning::
            This function only affects per-key backlighting featured connected devices.


        :param int key_code: The quartz-code of the ket to set
        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct
        """
        check_negative((red_percentage, green_percentage, blue_percentage))
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)

        return execute(
            self.led_dll.LogiLedSetLightingForKeyWithQuartzCode,
            key_code,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_for_key_with_scan_code(
        self, key_code, red_percentage, green_percentage, blue_percentage
    ):
        """
        Sets the key identified by the scancode passed as parameter to the desired color

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_code: The scan-code of the ket to set
        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct
        """
        check_negative((red_percentage, green_percentage, blue_percentage))
        check_maximum((red_percentage, green_percentage, blue_percentage), 100)

        return execute(
            self.led_dll.LogiLedSetLightingForKeyWithScanCode,
            key_code,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_from_bitmap(self, bitmap):
        """
        Sets the array of bytes passed as parameter as colors.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param char bitmap: An unsigned char array containing the colors to assign to each key
        """
        bitmap = ctypes.c_char_p(bitmap)
        return execute(self.led_dll.LogiLedSetLightingFromBitmap, bitmap)

    def set_target_device(self, target_device):
        """
        The function sets the target device type for future calls.
        By default, target device is all logitech device, therefore, if no call is made to LogiLedSetTargetDevice
        the SDK will apply any function to all the connected devices.

        :param int target_device:
        """

        return execute(self.led_dll.LogiLedSetTargetDevice, target_device)

    def stop_effects_on_key(self, key_name):
        """
        Stops any ongoing effect on the key passed in as parameter.

        .. warning::
            This function only affects per-key backlighting featured connected devices.
        """
        return execute(self.led_dll.LogiLedStopEffectsOnKey, key_name)


led_dll = None


def load_dll():
    global led_dll
    prev_cwd = Path(__file__).parent
    path_dll = f"{prev_cwd}/dll/LogitechLedEnginesWrapper.dll"
    if os.path.exists(path_dll):
        led_dll = ctypes.cdll.LoadLibrary(path_dll)
        if not bool(led_dll.LogiLedInit()):
            raise LGHUBNotLaunched(
                "You must start Logitech GHUB before using the Logipy packages"
            )
        return True
    else:
        raise SDKNotFoundException("The SDK DLL was not found.")
