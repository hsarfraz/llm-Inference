
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
- Python 3.11 
- uvicorn and fastapi 

```diff
version: "3.8"
 
services:

```
## Deploy 
Once the changes have been made to the [`docker-compose.yml`](./02_tiny_inference_single_model/docker-compose.yml) file to reflect your local environment. The containers can be build and deployed using below commands:

```bash
docker compose build
docker compose up -d
```
Given below is typical output upon successful running of tiny inference server
![image](https://github.com/hsarfraz/llm-Inference/assets/127702575/97009884-9628-41f9-912f-ff662c7d1645)

Also, below docker ps command can also be used to verify if tiny inference server is up and running
```bash
docker ps 
```
```bash
http://<HOST IP ADDRESS>/
```
Given below is a screen shot of the Chat UI working with tiny llm server

![image](https://github.com/hsarfraz/llm-Inference/assets/127702575/2ea748ba-f190-40ec-abd7-f6b5d386fc0a)