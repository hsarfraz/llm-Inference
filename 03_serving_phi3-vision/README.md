
# Inference using Microsoft phi3-vision model
Microsoft Phi3 vision language model is latest state-of-the art langauge model. This repo provides implementation of python/flask based web server to host model on premise for runtime inference. It provides examples to perform OCR and other functions using command line utlities like curl. The tiny Phi3-vision inference server is a simplified implementation to host model on-premise. It is designed for small scale inference deployments with max serving capacity for 1-5 users. 

It provides a simple REST based interface to allow utlization of the model. Inference server is based on a single Docker container that provides following key capabilities: 

1. Phi-3 model Inference
2. REST APIs for integration with llm
3. Support for quantized models

## Deliverables
- REST Interface to allow interaction with Phi-3 model
- Inference server configuration and setup 

## Supported Models

| Models              | OCR  | CUDA | 
| :------------------ | -----| :--: | 
| Phi-3-vision        | yes  |  ✅  | 
| Phi-3-medium        | no   |  ✅  | 
| Phi-3-small         | no   |  ✅  | 
| Phi-3-mini          | no   |  ✅  | 

## Requirement
- Linux server with GPU and CUDA Support
- Docker 
- Pytorch, Transformers, flash-attn
- uvicorn and fastapi 

```diff
version: "3.8"
services:
  phiserv:
    build:
      context: ./app
    container_name: phiserv
    hostname: phiserv
    environment:
      MODEL: microsoft/Phi-3-vision-128k-instruct
    ports:
      - "5000:5000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]  
    volumes:
      - ./model/:/root/.cache/huggingface  

```
## Deploy 
Once the changes have been made to the [`docker-compose.yml`](./02_tiny_inference_single_model/docker-compose.yml) file to reflect your local environment. The containers can be build and deployed using below commands:

```bash
docker compose build

docker compose up
or
docker compose up -d
```
Given below is typical output upon successful running of phi3-vision inference server
![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/phi3_container_running.png)

Also, below docker ps command can also be used to verify if tiny inference server is up and running
```bash
docker ps 
```
```bash
http://<HOST IP ADDRESS>:5000/
```
## Usage 
To perform OCR using the Phi3-vision model, the server has REST end point /ocr. This end point handles OCR of a single file using default prompt or custom prompt. The end point will return text of the uploaded image. Given below are few examples of calling the /ocr end point using curl. 

```bash
curl -F "file=@<replace_with_image_filename>.png" http://<host ip address>:5000/ocr
```

Contact me on freelancing web sites for assistance https://www.freelancer.com/u/hsarfraz76 or https://www.upwork.com/freelancers/~0178ad46e2372c8fe5 