#! /bin/bash

THIS_DIR=$(cd $(dirname $0); pwd)

PROJECT_ROOT=$(cd $THIS_DIR/..; pwd)

cd $PROJECT_ROOT && rm -rf *.egg-info && pip uninstall practices
