# Large language models (LLMs) Inference
Setting up Llama LLM inference On-Premise Environment

Large language models (LLMs) are a powerful tool with the potential to revolutionize a wide range of industries. However, deploying and managing LLMs can be a complex and challenging task. This repo provides implemented details to perform LLMs in an on-premise environment. 

## Option No 1: LLM Inference Server – Using Huggingface TGI

## Option No 1: LLM Inference Server with Custom REST APIs




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
