import os
import json
import fastapi
import uvicorn
import gradio as gr

from ctransformers import AutoModelForCausalLM
from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
# from slowapi.middleware import SlowAPIMiddleware

stemp = os.environ['MODEL_INDEX']

model_index = int(stemp)
dir_conf = os.getcwd() + '/config.json'

with open(dir_conf) as f:
    d = json.load(f)
    # print(d)

count = 0
for i in d['loader']:
    if count==model_index:
        model_file = i['model_file']
        model_type = i['model_type']
        gpu_layers = i['gpu_layers']
    count = count + 1

print('model_file=', model_file)
print('model_type=', model_type)
print('gpu_layers=', gpu_layers)

# check ctransformers doc for more configs
config = {'max_new_tokens': 256, 'repetition_penalty': 1.1,'temperature': 0.1, 'stream': True}

llm = AutoModelForCausalLM.from_pretrained(model_file,model_type=model_type,gpu_layers=120,**config)
print('model loaded...')

# limiter = Limiter(key_func=get_remote_address)
app = fastapi.FastAPI(title="TinyServer")
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to format prompt according to Llama2 expected chat instruction format
def format_prompt(prompt: str):
    llama_template =f"""[INST]{prompt}[/INST]"""
    return llama_template

@app.get("/generate")
async def generatemsg(message,history):
    prompt = format_prompt(message)
    retmsg = llm(prompt, stream=False)
    return retmsg


@app.get("/stream")
def streamsg(message,history):
    tokens = llm.tokenize(message)
    retmsg =''
    for chat_chunk in llm.generate(tokens,temperature=0.1,repetition_penalty=1.1,):
        if chat_chunk == llm.is_eos_token:
            return 
        retmsg = retmsg + '' + llm.detokenize(chat_chunk)
        yield str(retmsg)


io = gr.ChatInterface(
    generatemsg,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Chat with me!", container=False, scale=7),
    description="This is the demo of Tiny Inference Server with " + model_file,
    title="Tiny Inference Server",
    examples=["Are tomatoes vegetables?"],
    retry_btn="Retry",
    undo_btn="Undo",
    clear_btn="Clear",
)

@app.get("/health_check")
async def health_check():
    return "ok"

if __name__ == "__main__":
  demo = gr.mount_gradio_app(app, io, path='/')  
  uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)