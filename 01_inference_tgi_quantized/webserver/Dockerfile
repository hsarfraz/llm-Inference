FROM python:3.11-slim-buster
# RUN mkdir /app
# ADD . /app
WORKDIR /

COPY requirements.txt ./
COPY ui3.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "ui3.py" ]