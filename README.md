
![](https://clarence.engineer/storage/2024/07/cropped-Frame-9-192x192.png)


### Introduction

[Probably] a work in progress for a WhatsApp AI personal assistant that can automate tasks, reminders, collect ideas, note important stuff, personal finance tracking and much more.

### Currently Available Features

- Transcribe WhatsApp Voice Notes To Text.

### Currently Used Technologies

- Flask Server
- Open AI Whisper Model [tested with python 3.10, may cause issues with 3.13]
- GPT4 Model (Soon)

### How to run

#### 1. Environment variables

You could constitute a `.env` file with the following parameters:

```
# This is a sample content of the env file.
OPENAI_API_KEY = # generated in the OpenAI platform portal (platform.openai.com)
WHATSAPP_ACCESS_TOKEN =    # Generated in the WhatsApp Developer portal
WHATSAPP_PHONENUMBER_ID =    # Given by WhatsApp in your portal
WHATSAPP_BUSINESS_ID =    # Given by WhatsApp in your portal
WHATSAPP_GRAPH_VERSION =  "v20.0" # the version of the  API 
WHATSAPP_WEBHOOK_TOKEN =  # for webhook verification, provided by you when creating the webhook. You can run the `gentoken.py` file.
```

#### Direct Run 

```
#!/bin/bash

# Do brew install ffmpeg if on macos
sudo apt-get install -y ffmpeg 

python3 -m venv ./venv

source ./venv/bin/activate

python3 -m pip install -r requirements.txt

python3 -m pip install  "git+https://github.com/openai/whisper.git"

#just to cache the model initially.
python3 downloadmodel.py 

# generate the token (if you want). The token is used for the WhatsApp Cloud API webhook
python3 gentoken.py 

python3 run.py

```

#### Using Docker

```
#!/bin/bash

# Stop and remove any existing container
docker stop wa-voice 2>/dev/null || true
docker rm wa-voice 2>/dev/null || true

# Build the image
docker build -t wa-voice:latest .

# Run the container
docker run -d -p 8085:8085 --name wa-voice wa-voice:latest

# Display running containers
docker ps
```
