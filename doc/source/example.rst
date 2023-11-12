.. currentmodule:: logi_led


Example
=======

1. Change keyboard color when key is pressed

.. literalinclude:: example/color_key_pressed.py
  :language: python

.. note::
    To exit program you need to press ``ESC`` key. You can change this key by anything you want.
    You can refer to `keyboard.Key <https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key>`_
    for special character or ``key.char`` for alphanumeric value.

.. warning::
    This example will not work if you don't have `pynput <https://pypi.org/project/pynput/>`_ installed.
    You can install it by ``pip install pynput``