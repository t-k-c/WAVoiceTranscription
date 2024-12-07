# Let's use python 3.10. The rest is the basic docker approach 101 :)
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    gcc \
    libc-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir "git+https://github.com/openai/whisper.git"

COPY . .

EXPOSE 8085

CMD ["python","run.py"]
