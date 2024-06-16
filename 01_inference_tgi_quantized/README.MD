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

