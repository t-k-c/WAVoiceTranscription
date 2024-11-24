# Let's use python 3.13. The rest is the basic docker approach 101 :)
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

COPY . .

EXPOSE 5000

CMD ["python","run.py"]