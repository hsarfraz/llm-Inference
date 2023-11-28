# Large Language Models (LLMs) Inference
Setting up LLM inference services within data centers and/or on-premise environments.

Large language models (LLMs) are a powerful tool with the potential to revolutionize a wide range of industries. However, deploying and managing LLMs on-premise can be a complex and challenging task. This repo provides ready to deploy configuration and python code for setting up of llm inference servers. This includes REST API and web interface to chat with llm models. The implementation is based on docker containers. 

The focus is primarily on runtime inference, it does not cater for fine-tuning and training of llm. The model serving includes original model and/or quantized versions. 

- [Inference using Hugging Face TGI & Web Chat Interface](#inference-using-hugging-face-tgi-&-web-chat-interface)

- [Inference using Tiny LLM Server & Web Chat Interface](02_tiny_inference_single_model)

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

