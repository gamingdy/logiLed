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

All LogitechLed functions are available when you use NotTested. Allowing you to use both simultaneously

.. note::
    The full list of functions is available here :doc:`logipy`

Best way to stop program
~~~~~~~~~~~~~~~~~~~~~~~~

.. important::
    To terminate a program correctly, we recommend using the LogitechLed instance's shutdown function

    .. code-block:: python

        logi_led.shutdown()

You can go to :doc:`example` to see what you can do with it.