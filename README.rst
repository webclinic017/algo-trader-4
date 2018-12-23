algotrader
==========


Usage
-----

::

  python -m algotrader.cli --signal-source file --filename test.json --worker signal-consumer --config-file config_dev.yaml


Install setup.py
----------------

We can create a package and then run it;

::

  python setup.py install
  algotrader --worker signal-consumer --filename test.json --config-file config_dev.yaml --signal-source file