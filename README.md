# Large Language Models (LLMs) Inference
Setting up LLM inference services within data centers and/or on-premise environments.

Large language models (LLMs) are a powerful tool with the potential to revolutionize a wide range of industries. However, deploying and managing LLMs on-premise can be a complex and challenging task. This repo provides ready to deploy configuration and python code for setting up of llm inference servers. This includes REST API and web interface to chat with llm models. The implementation is based on docker containers. 

The focus is primarily on runtime inference, it does not cater for fine-tuning and training of llm. The model serving includes original model and/or quantized versions. 

- [Inference using Hugging Face TGI & Web Chat Interface](#inference-using-hugging-face-tgi-&-web-chat-interface)

- [Inference using Tiny LLM Server & Web Chat Interface](#Inference-using-Tiny-llm-Server-&-Web-Chat-Interface)

## Three Tier Architecture - LLM Inference:
Three tier architecture for llm inference is used to perform on premise deployment. This architecture allows greater flexibility and agility. It is assumed that on premise hosting infrastructure is behind firewalls with no outbound connectivity to internet as part of security policies. 


1. Backend llm inference server 
2. Web application server
3. Front-end using web browser

![image](https://github.com/hsarfraz/llm-Inference/assets/127702575/d33e7c08-ef50-4ced-b0d1-e35568bd7f6d)

# Inference using Hugging Face TGI & Web Chat Interface
This section provides details on deployment of three tier llm inference architecture using Hugging Face TGI on local Linux environment. 

Comprehensive list of models that are supported by [TGI](https://huggingface.co/docs/text-generation-inference/supported_models) is provided by Hugging Face.

## Deliverables
- Web Interface to allow interaction with llm
- Inference server configuration and setup 
- Deployment of following models:
  - Code LLama 
  - LLama 2 
  - Falcon 

## Requirement
- Linux server with GPU's and CUDA Support
- Docker 
- Python 3.11 
- Gradio for UI

Copy files from folder '01_inference_tgi_quantized' to your local Linux GPU server. Adjust Docker compose file [`docker-compose.yml`](./01_inference_tgi_quantized/docker-compose.yml) to local Linux environment as highlighted below:

```diff
version: "3.8"
 
services:
  tgi:
    image: ghcr.io/huggingface/text-generation-inference
    container_name: infer
    ports:
      - "8080:80" 
    networks:
      - tracenet
    volumes: 
-      - /media/ms/DATA/text-generation-inference/data:/data
+      - <LOCAL FOLDER PATH>:/data
      - /tmp:/tmp             
    environment:
-      - MODEL_ID=/data/CodeLlama-7B-GPTQ
+      - MODEL_ID=<QUANTIZED GPTQ MODEL>
      - NUM_SHARD=1
      - QUANTIZE=gptq
      - SHM-SIZE=1g
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  web:
      build:
        context: ./webserver
      container_name: webserve
      depends_on:
        - "tgi"        
      ports:
        - "80:8003"   
      networks:
        - tracenet              
      volumes:
          - .:/app              
networks:
   tracenet:               
```

## Deploy 
Once the changes have been made to the [`docker-compose.yml`](./01_inference_tgi_quantized/docker-compose.yml) file to reflect your local environment. The containers can be build and deployed using below commands:

```bash
docker compose build
docker compose up -d
```

After deployment TGI REST API are accessible via 
```bash
http://<HOST IP ADDRESS>:8080/
```
Gradio web UI to chat with llm is made accessible via
```bash
http://<HOST IP ADDRESS>/
```



# Inference using Tiny llm Server & Web Chat Interface
The tiny llm inference server is a simplified implementation to host llm modles on-premise. It is designed for small scale inference deployments with max serving capacity for 1-5 users. Tiny llm inference server is based on a single Docker container that provides following key capabilities: 

1. llm Inference
2. Ability to host multiple models on GPU
3. Split model layers between GPU and host RAM
4. Embedded Web UI for End User using Gradio
5. REST APIs for integration with llm
6. Support for quantized models

## Deliverables
- Web Interface to allow interaction with llm
- Inference server configuration and setup 

## Supported Models

| Models              | Model Type    | CUDA | 
| :------------------ | ------------- | :--: | 
| GPT-2               | `gpt2`        |      | 
| GPT-J, GPT4All-J    | `gptj`        |      | 
| GPT-NeoX, StableLM  | `gpt_neox`    |      | 
| Falcon              | `falcon`      |  ✅  |  
| LLaMA, LLaMA 2      | `llama`       |  ✅  |
| Code LLaMA          | `llama`       |  ✅  |
| MPT                 | `mpt`         |  ✅  |
| StarCoder, StarChat | `gpt_bigcode` |  ✅  |
| Dolly V2            | `dolly-v2`    |      |
| Replit              | `replit`      |      |

## Requirement
- Linux server with single GPU and CUDA Support
- Docker 
- Python 3.11 
- Gradio for UI
- uvicorn and fastapi 

```diff
version: "3.8"
 
services:
  webtiny1:
    build:
      context: ./webserver
    container_name: webtiny1 
    volumes: 
-      - /media/ms/DATA/models:/data
+      - <LOCAL FOLDER PATH>:/data
      - /tmp:/tmp     
    environment:
      - MODEL_INDEX=0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]                  
    ports:
      - "80:8000"
    networks:
      - tinynet              
networks:
  tinynet: 


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
![image](https://github.com/hsarfraz/llm-Inference/assets/127702575/9643a105-b7a8-49d6-bcd1-90827719e8cb)
## Chat UI - Tiny llm Server

Gradio web UI to chat with llm is made accessible via
```bash
http://<HOST IP ADDRESS>/
```
Given below is a screen shot of the Chat UI working with tiny llm server

![image](https://github.com/hsarfraz/llm-Inference/assets/127702575/2ea748ba-f190-40ec-abd7-f6b5d386fc0a)