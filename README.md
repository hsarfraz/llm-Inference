# Large language models (LLMs) Inference
Setting up Llama LLM inference On-Premise Environment

Large language models (LLMs) are a powerful tool with the potential to revolutionize a wide range of industries. However, deploying and managing LLMs can be a complex and challenging task. This repo provides implemented details to perform LLMs in an on-premise environment. 

## Option No 1: On-Premise llm inference using Huggingface TGI
## Option No 2: LLM Inference Server with Custom REST APIs


# Option No 1: On-Premise llm inference using Huggingface TGI
Three tier architecture for llm inference is perform deployment on premise. This architecture allows greater flexibility and agility. It is assumed that on premise hosting infrastructure is behind firewalls with no outbound connectivity to internet as part of security policies. 

The three tiers consists of following:
1: Backend llm inference server – huggingface TGI server
2: Web application server
3: Front-end using web browser

## Deliverables
- Web Interface to allow interaction with llm
- Deployment of following models:
  - Code LLama 7B, 13B 
  - LLama 7B
  - Falcon 7B

## Requirement
- docker
- Python 3.11 

# Option No 1: LLM Inference Server with Custom REST APIs
The basic implementation of an inference server requires the following components:
- Embedded Web UI for End User
- Provide REST APIs for external client usage
- Ability to load interact with LLM Model
- GPU with enough RAM to load the LLM model

## Requirement

- Python 3.10+ 
- Transformers, Datasets, Accelerate, PEFT and TRL
- gradio (used in web_demo.py)
- uvicorn and fastapi (used in api_demo.py)

- 
