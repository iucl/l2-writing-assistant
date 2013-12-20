#!/bin/bash

virtualenv -p /usr/bin/python3 venv
. venv/bin/activate
pip install https://github.com/kpu/kenlm/archive/master.zip
