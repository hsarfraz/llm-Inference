
import os
from os.path import join, dirname

import time
import numpy as np
from datetime import datetime

from dotenv import load_dotenv

# Import necessary libraries
import cv2
from PIL import Image

import torch
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor
from transformers import BitsAndBytesConfig

from concurrent.futures import ProcessPoolExecutor

import asyncio
from typing import Annotated, Union
from fastapi import FastAPI, UploadFile, Form, Response, Request, Depends, status,File
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware

import uvicorn

# load configuration from env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# load environment variable 
env_model = os.environ.get("MODEL")
env_model = 'microsoft/Phi-3-vision-128k-instruct' if env_model is None else env_model


app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])


model = None
processor = None

# load phi3-vision model
def create_model():
    global model
    global processor    

    # Load processor
    processor = AutoProcessor.from_pretrained(env_model, trust_remote_code=True)

    # Define BitsAndBytes configuration for 4-bit quantization
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    # Load model with 4-bit quantization and map to CUDA
    model = AutoModelForCausalLM.from_pretrained(
        env_model,
        device_map="cuda:0",
        trust_remote_code=True,
        torch_dtype="auto",
        # quantization_config=nf4_config, 
    )

    # evaluate model
    model.eval() 


def model_predict(prompt,im_pil):
    ts = time.time()
    # vector = sbertmodel.encode('How big is London')
    inputs = processor(prompt, [im_pil], return_tensors="pt").to("cuda:0")
    # Generate text response using model
    generate_ids = model.generate(
        **inputs,
        eos_token_id=processor.tokenizer.eos_token_id,
        max_new_tokens=1500,
        do_sample=False,
    )    
    # Remove input tokens from generated response
    generate_ids = generate_ids[:, inputs["input_ids"].shape[1] :]

    # Decode generated IDs to text
    response = processor.batch_decode(generate_ids, skip_special_tokens=False, clean_up_tokenization_spaces=True)[0]

    return response


# setup process pooling
pool = ProcessPoolExecutor(max_workers=1, initializer=create_model)


# ----
user_prompt = '<|user|>\n'
assistant_prompt = '<|assistant|>\n'
prompt_suffix = "<|end|>\n"



# FRONTEND
@app.get('/')
async def home():
    return PlainTextResponse('Phi3-Vision OCR.', status_code=status.HTTP_200_OK) 

@app.post("/ocr")
async def get_ocr_json(file: Union[UploadFile, None] = None, prompt: Annotated[str, Form()]=None):

    # Validate 
    if file == None:
        return PlainTextResponse('Upload file for OCR...', status_code=status.HTTP_400_BAD_REQUEST) 

    # prepare prompt - default if not provided
    if prompt == None or len(prompt) < 5:
        prompt = user_prompt + "<|image_1|>\nOCR the text of the image as is OCR:" + prompt_suffix #+ assistant_prompt
    else:
        prompt =  user_prompt + "<|image_1|>\n" + prompt + prompt_suffix #+ assistant_prompt

    # get process id
    worker_pid = os.getpid()
    print(f"Handling OCR request with worker PID: {worker_pid}")

    try:
        loop = asyncio.get_event_loop()
        start_time = time.time()
        # get image
        img = cv2.imdecode(np.frombuffer(file.file.read(), np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        # worker should be initialized outside endpoint to avoid cold start
        response = await loop.run_in_executor(pool, model_predict,prompt,im_pil)

        end_time = time.time()
        processing_time = end_time - start_time

        print(f"Processing Time: {processing_time}")        

        return str(response)
    except Exception as e:
        return PlainTextResponse(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)        

if __name__ == "__main__":
   uvicorn.run("serve_phi_fastapi:app", host="0.0.0.0", port=5000, reload=False)

