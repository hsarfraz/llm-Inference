
# Inference using Tiny llm Server & Web Chat Interface
The tiny LLM inference server is a simplified implementation to host LLM models on-premise. It is designed for small scale inference deployments with max serving capacity for 1-5 users. Tiny llm inference server is based on a single Docker container that provides following key capabilities: 

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