#!/bin/bash
if [[ $1 == 'train' ]]; then
  python /code/train.py
else
  python /code/app.py
fi

