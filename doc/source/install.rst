:orphan:


Installing LogiLed
==================

You can get the library directly from PyPI:

.. code:: sh

    $ pip install logiled

If pip command not found

.. code:: sh

    $ python -m pip install logiled



Virtual Environement
~~~~~~~~~~~~~~~~~~~~

Sometimes you want to keep libraries from polluting system installs or use a different version of libraries than the ones installed on the system

A more in-depth tutorial is found on `Virtual Environments and Packages <https://docs.python.org/3/tutorial/venv.html>`_


However, for the quick and dirty:


1. Go to your project's working directory:

    .. code-block:: sh

        $ cd your-projet-source
        $ python -m venv .venv

2. Activate the virtual environment:

    .. code-block:: sh

        $ .venv\Scripts\activate.bat

3. Use pip like usual:

    .. code-block:: sh

        $ pip install logiled

Congratulations. You now have a virtual environment all set up.

---------

Once installed, you can go and see how it's used :doc:`usage`
