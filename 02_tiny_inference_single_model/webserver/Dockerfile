FROM nvcr.io/nvidia/pytorch:23.10-py3
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY llmserve.py ./
COPY config.json ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "llmserve.py" ]