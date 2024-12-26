#!/bin/bash

#python3.10

# brew install ffmpeg if on macos
sudo apt-get install -y ffmpeg 

python3 -m venv ./venv

source ./venv/bin/activate

python3 -m pip install -r requirements.txt

python3 -m pip install  "git+https://github.com/openai/whisper.git"

#just to cache the model initially.
python3 downloadmodel.py 

# generate the token (if you want)
python3 gentoken.py 

python3 app.py