#!/bin/bash

if [ -z "$ENV_NAME" ]; then
    echo "ENV_NAME is not set"
    exit 1
fi

ENV_LIST=`conda env list | awk '{print $1}' | grep -v '^#'`

if [[ $ENV_LIST =~ $ENV_NAME ]]; then
    echo "Environment $ENV_NAME already exists"
    exit 1
fi

conda create -n $ENV_NAME python=3.10 -y