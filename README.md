# LogiLed

> [!IMPORTANT]  
> This package is not affiliated with Logitech.
> It has been designed to allow anyone to customize the RGB of these devices.
>
> This project is a fork of LogiPy, the original code can be found [here](https://github.com/Logitech/logiPy)

Use the LED SDK to access all LED and RGB backlight functions and features of Logitech G products.
Integrate profiles for custom key configurations, develop in-game effects, or mark keys to keep track of
cool downs on various commands.

## Documentation

The documentation can be found [here](https://logiled.gamingdy.me/en/latest/).  
You can found the test documentation [here](https://beta.logiled.gamingdy.me/en/latest/).

## Installation

```sh
pip install logiled
```

Install the test version:

```sh
pip install -i https://test.pypi.org/simple/ logiled
```

## LED Examples

Set all device lighting to red:

```py
from logiled import LogitechLed, load_dll

load_dll()

led = LogitechLed()

led.set_lighting(100, 0, 0)
input("Press enter to shutdown SDK...")
led.shutdown()
```
