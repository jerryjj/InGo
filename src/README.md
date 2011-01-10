# InGo

## Installation

### Prepare virtual environment

Without local virtualenv:
    $ curl http://ingo.infigo.fi/downloads/current/ingo-install.py | python - ingoenv
OR
With local virtualenv:
    $ virtualenv --no-site-packages ingoenv

Activate the virtual environment:
    $ source ingoenv/bin/activate

### Installation from source

$ git clone http://github.com/...
$ cd InGo/src
$ python setup.py develop

### Installation from PyPi

$ easy_install -i http://www.turbogears.org/2.0/downloads/current/ InGo