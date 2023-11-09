"""
.. note::
    logi_led.py : Defines the exported functions for the API Logitech Gaming LED SDK
    Original author: **Tom Lambert**

    This is a fork of https://github.com/Logitech/logiPy by **gamingdy**
"""

import ctypes
import os
from pathlib import Path


class SDKNotFound(BaseException):
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
    """
    Raised if connection with Logitech SDK is lost
    """

    pass


class DLLNotLoad(BaseException):
    """
    Raised if DLL is not load
    """

    pass


def check_value(minimum, maximum, *values):
    for value in values:
        if value < minimum:
            raise RangeError(f"Value can't be lower than {minimum}")
        elif value > maximum:
            raise RangeError(f"Value can't be greater than {maximum}")


def execute(funct, *args):
    result = funct(*args)
    if result:
        return True

    raise ConnectionLost(
        f"Connection with Logitech SDK is lost, try to restart LogitechGHub"
    )


def check_type(type_name, *values):
    for value in values:
        if not isinstance(value, type_name):
            raise TypeError(f"Value {value} must be a {type_name}")


class LogitechLed:
    """
    .. note::
        The following class is the main class of library
    """

    def __init__(self):
        if led_dll is None:
            raise DLLNotLoad(
                "You must load DLL before using the Logipy packages"
            )
        self.led_dll = led_dll

    def shutdown(self):
        """
        Restores the last saved lighting and frees memory used by the SDK.
        """
        execute(self.led_dll.LogiLedShutdown)

    def save_current_lighting(self):
        """
        Saves the current lighting so that it can be restored after a temporary effect is finished.

        .. note::
            On per-key backlighting supporting devices, this function will save the current state for each key.
        """
        execute(self.led_dll.LogiLedSaveCurrentLighting)

    def set_lighting(
        self, red_percentage: int, green_percentage: int, blue_percentage: int
    ):
        """
        Sets the lighting on connected and supported devices.

        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct
        :raises TypeError: Raised if bad type is passed as parameter

        """
        check_type(int, red_percentage, green_percentage, blue_percentage)
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)

        execute(
            self.led_dll.LogiLedSetLighting,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def flash_lighting(
        self,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
        ms_duration: int,
        ms_interval: int,
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
        :raises TypeError: Raised if bad type is passed as parameter

        .. tip::
            Specifying a **ms_duration** to 0 will cause the effect to be infinite until reset
        """
        check_type(
            int,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)
        check_value(0, float("inf"), ms_duration, ms_interval)

        execute(
            self.led_dll.LogiLedFlashLighting,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )

    def pulse_lighting(
        self,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
        ms_duration: int,
        ms_interval: int,
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
        :raises TypeError: Raised if bad type is passed as parameter

        .. tip::
            Specifying a **ms_duration** to 0 will cause the effect to be infinite until reset
        """
        check_type(
            int,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)
        check_value(0, float("inf"), ms_duration, ms_interval)

        execute(
            self.led_dll.LogiLedPulseLighting,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )

    def stop_effects(self):
        """
        Stops any of the presets effects (started from :func:`flash_lighting` or :func:`pulse_lighting`).
        """
        execute(self.led_dll.LogiLedStopEffects)

    def set_lighting_for_target_zone(
        self,
        zone: int,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
    ):
        """
        Sets lighting on a specific zone for all connected zonal devices that match the device type

        :param int zone: Zone id on target device
        :param int red_percentage: Amount of red. **Range is 0 to 100**.
        :param int green_percentage: Amount of green. **Range is 0 to 100**.
        :param int blue_percentage: Amount of blue. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct
        :raises TypeError: Raised if bad type is passed as parameter

        """
        check_type(int, zone, red_percentage, green_percentage, blue_percentage)
        check_value(
            0, 100, zone, red_percentage, green_percentage, blue_percentage
        )
        execute(
            self.led_dll.LogiLedSetLightingForTargetZone,
            None,
            zone,
            red_percentage,
            green_percentage,
            blue_percentage,
        )


class NotTested(LogitechLed):
    """
    .. warning::
        A list of untested functions, which can be used but for which we are not sure of the correct operation.
    """

    def __init__(self):
        super().__init__()

    def flash_single_key(
        self,
        key_name: int,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
        ms_duration: int,
        ms_interval: int,
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
        :raises TypeError: Raised if bad type is passed as parameter

        .. tip::
            Specifying a **ms_duration** to 0 will cause the effect to be infinite until reset
        """
        check_type(
            int,
            key_name,
            red_percentage,
            green_percentage,
            blue_percentage,
            ms_duration,
            ms_interval,
        )
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)
        check_value(0, float("inf"), ms_duration, ms_interval)
        execute(
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
        key_name: int,
        red_percentage_start: int,
        green_percentage_start: int,
        blue_percentage_start: int,
        ms_duration: int,
        is_infinite: bool = False,
        red_percentage_end: int = 0,
        green_percentage_end: int = 0,
        blue_percentage_end: int = 0,
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
        :param bool is_infinite: If set to True, it will loop infinitely until stopped with a called to
                                :func:`stop_effects_on_key` or :func:`stop_effects <LogitechLed.stop_effects>`
        :param int red_percentage_end: Amount of red in the finish color of the effect. **Range is 0 to 100**.
        :param int green_percentage_end: Amount of green in the finish color of the effect. **Range is 0 to 100**.
        :param int blue_percentage_end: Amount of blue in the finish color of the effect. **Range is 0 to 100**.

        :raises RangeError: Raised if color percentage range is not correct
        :raises TypeError: Raised if bad type is passed as parameter

        """
        check_type(
            int,
            key_name,
            red_percentage_start,
            green_percentage_start,
            blue_percentage_start,
            ms_duration,
            red_percentage_end,
            green_percentage_end,
            blue_percentage_end,
        )
        check_type(bool, is_infinite)
        check_value(
            0,
            100,
            red_percentage_start,
            green_percentage_start,
            blue_percentage_start,
            red_percentage_end,
            green_percentage_end,
            blue_percentage_end,
        )
        check_value(0, float("inf"), ms_duration)
        execute(
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
        execute(self.led_dll.LogiLedRestoreLighting)

    def restore_lighting_for_key(self, key_name: int):
        """
        Restores the saved color on the key passed as argument.
        Use this function with the :func:`save_lighting_for_key` to preserve
        the state of a key before applying any effect.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_name: The key to restore the color on.

        :raises TypeError: Raised if bad type is passed as parameter
        """
        check_type(int, key_name)
        execute(self.led_dll.LogiLedRestoreLightingForKey, key_name)

    def save_lighting_for_key(self, key_name: int):
        """
        Saves the current color on the keycode passed as argument.
        Use this function with the :func:`restore_lighting_for_key`
        to preserve the state of a key before applying any effect.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param int key_name: The key to save the color for.

        :raises TypeError: Raised if bad type is passed as parameter

        """
        check_type(int, key_name)
        execute(self.led_dll.LogiLedSaveLightingForKey, key_name)

    def set_lighting_for_key_with_hid_code(
        self,
        key_code: int,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
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
        :raises TypeError: Raised if bad type is passed as parameter
        """
        check_type(
            int, key_code, red_percentage, green_percentage, blue_percentage
        )
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)

        execute(
            self.led_dll.LogiLedSetLightingForKeyWithHidCode,
            key_code,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_for_key_with_key_name(
        self,
        key_name: int,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
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
        :raises TypeError: Raised if bad type is passed as parameter
        """
        check_type(
            int, key_name, red_percentage, green_percentage, blue_percentage
        )
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)

        execute(
            self.led_dll.LogiLedSetLightingForKeyWithKeyName,
            key_name,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_for_key_with_quartz_code(
        self,
        key_code: int,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
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
        :raises TypeError: Raised if bad type is passed as parameter
        """
        check_type(
            int, key_code, red_percentage, green_percentage, blue_percentage
        )
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)

        execute(
            self.led_dll.LogiLedSetLightingForKeyWithQuartzCode,
            key_code,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_for_key_with_scan_code(
        self,
        key_code: int,
        red_percentage: int,
        green_percentage: int,
        blue_percentage: int,
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
        :raises TypeError: Raised if bad type is passed as parameter
        """
        check_type(
            int, key_code, red_percentage, green_percentage, blue_percentage
        )
        check_value(0, 100, red_percentage, green_percentage, blue_percentage)

        execute(
            self.led_dll.LogiLedSetLightingForKeyWithScanCode,
            key_code,
            red_percentage,
            green_percentage,
            blue_percentage,
        )

    def set_lighting_from_bitmap(self, bitmap: bytes):
        """
        Sets the array of bytes passed as parameter as colors.

        .. warning::
            This function only affects per-key backlighting featured connected devices.

        :param bytes bitmap: An unsigned char array containing the colors to assign to each key
        :raises TypeError: Raised if bad type is passed as parameter
        """
        check_type(bytes, bitmap)
        bitmap = ctypes.c_char_p(bitmap)
        execute(self.led_dll.LogiLedSetLightingFromBitmap, bitmap)

    def set_target_device(self, target_device: int):
        """
        The function sets the target device type for future calls.
        By default, target device is all logitech device, therefore, if no call is made to LogiLedSetTargetDevice
        the SDK will apply any function to all the connected devices.

        :param int target_device:

        :raises TypeError: Raised if bad type is passed as parameter
        """
        check_type(int, target_device)
        execute(self.led_dll.LogiLedSetTargetDevice, target_device)

    def stop_effects_on_key(self, key_name: int):
        """
        Stops any ongoing effect on the key passed in as parameter.

        :param int key_name: The ket to sto the efects on

        :raises TypeError: Raised if bad type is passed as parameter

        .. warning::
            This function only affects per-key backlighting featured connected devices.
        """
        check_type(int, key_name)
        execute(self.led_dll.LogiLedStopEffectsOnKey, key_name)


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
        raise SDKNotFound("The SDK DLL was not found.")
