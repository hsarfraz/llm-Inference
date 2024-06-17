import json
import os
from os.path import join, dirname
import cv2
import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from datetime import datetime
import aiohttp
import asyncio
import requests
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

# Import necessary libraries
from PIL import Image
import requests
import torch
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor
from transformers import BitsAndBytesConfig



# load configuration from env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 #to allow upload of big images via flask
    return app


app = create_app()

JWTManager(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}}) # Allow all origins

# ---
env_model = os.environ.get("MODEL")
env_model = 'microsoft/Phi-3-vision-128k-instruct' if env_model is None else env_model

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
    quantization_config=nf4_config,
)

# evaluate model
model.eval()

# FRONTEND
@app.route('/')
def home():
    return str('Phi3-Vision OCR'),200

@app.route('/ocr', methods=['POST'])
def get_ocr_json():
    if 'file' not in request.files:
        return jsonify({'status': 'File Not Uploaded'}), 400

    file = request.files['file']#.stream.read()

    # get all form elements from POST
    prompt = request.form.get('prompt') # Get the search query from request parameters        

    if prompt == None or len(prompt) < 5:
        prompt = [{"role": "user", "content": "<|image_1|>\nOCR the text of the image as is OCR:"}] 
    else:
        prompt = [{"role": "user", "content": "<|image_1|>\n" + prompt}] 

    # get process id
    worker_pid = os.getpid()
    print(f"Handling OCR request with worker PID: {worker_pid}")


    try:
        # messages = [{"role": "user", "content": "<|image_1|>\nOCR the text of the image as is OCR:"}]

        start_time = time.time()
        # call PaddleOCR model and get bytes of red line image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        # You may need to convert the color.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        # image = Image.open(i)
        # image = image.resize((1344, 1344))
        # Prepare prompt with image token
        prompt = processor.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)

        # Process prompt and image for model input
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
        response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        end_time = time.time()
        processing_time = end_time - start_time

        print(f"Processing Time: {processing_time}")        

        return str(response),200
    except Exception as e:
        return jsonify({'status': 500, "message": str(e)}), 500



def start_flask_app():
    app.run(host='0.0.0.0',debug=True, use_reloader=False)  # use_reloader=False to prevent the Flask app from starting twice

if __name__ == '__main__':

    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()

    # loop = asyncio.get_event_loop()
    # loop.create_task(start_async_watcher())
    # loop.run_forever()

