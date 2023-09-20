:orphan:

How to use Logipy
======================

.. important::
    Before reading this, please check that you have installed the module, if not, here's how to do it :doc:`install`


First you need to import the module and load the dll

.. code-block:: python

    import packagename

    packagename.load_dll()


Once dll is loaded, you can initialize LogitechLed

.. code-block:: python

    logi_led = packagename.LogitechLed()

Or NotTested if you want to use untested functions

.. code-block:: python

    logi_led_untested = packagename.NotTested()

It is also possible to initialize both, so that functions from both can be used.

.. code-block:: python

    logi_led = packagename.LogitechLed()
    logi_led_untested = packagename.NotTested()

.. note::
    The full list of functions is available here :doc:`logipy`


.. important::
    To terminate a program correctly, we recommend using the LogitechLed instance's shutdown function

    .. code-block:: python

        logi_led.shutdown()
