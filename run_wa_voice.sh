#!/bin/bash

#python3.10

sudo apt-get install -y ffmpeg # brew install ffmpeg if on macos

python3 -m venv ./venv

source ./venv/bin/activate

python3 -m pip install -r requirements.txt

python3 -m pip install  "git+https://github.com/openai/whisper.git"

python3 downloadmodel.py #just to cache the model.

python3 gentoken.py #generate the token (if you want)

python3 app.py