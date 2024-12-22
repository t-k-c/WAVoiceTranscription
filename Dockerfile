# Let's use python 3.10. The rest is the basic docker approach 101 :)
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install git -y

# Install ffmpeg 
RUN apt-get install -y ffmpeg

RUN pip install -r requirements.txt

RUN pip install  "git+https://github.com/openai/whisper.git"

COPY . .

EXPOSE 8085

CMD ["python","run.py"]
