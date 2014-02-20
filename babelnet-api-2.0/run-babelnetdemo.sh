#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
java -classpath babelnet-api-2.0.jar:lib/*:config it.uniroma1.lcl.babelnet.BabelNetDemo
