# Large Language Models (LLMs) Inference
Setting up LLM inference services within data centers and/or on-premise environments.

Large language models (LLMs) are a powerful tool with the potential to revolutionize a wide range of industries. However, deploying and managing LLMs on-premise can be a complex and challenging task. This repo provides ready to deploy configuration and python code for setting up of llm inference servers. This includes REST API and web interface to chat with llm models. The implementation is based on docker containers. 

The focus is primarily on runtime inference, it does not cater for fine-tuning and training of llm. The model serving includes original model and/or quantized versions. 

- [Inference using Hugging Face TGI & Web Chat Interface](01_inference_tgi_quantized)

- [Inference using Tiny LLM Server & Web Chat Interface](02_tiny_inference_single_model)

## Three Tier Architecture - LLM Inference:
Three tier architecture for llm inference is used to perform on premise deployment. This architecture allows greater flexibility and agility. It is assumed that on premise hosting infrastructure is behind firewalls with no outbound connectivity to internet as part of security policies. 


1. Backend llm inference server 
2. Web application server
3. Front-end using web browser

![image](https://github.com/hsarfraz/llm-Inference/assets/127702575/d33e7c08-ef50-4ced-b0d1-e35568bd7f6d)

