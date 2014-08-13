#!/bin/bash

## you may also need:
## sudo apt-get install libxslt1-dev

virtualenv -p /opt/local/bin/python3.3 venv
. venv/bin/activate
pip install https://github.com/kpu/kenlm/archive/master.zip
pip install lxml
