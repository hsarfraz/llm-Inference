import gradio as gr
import uvicorn
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient

client = InferenceClient(model="http://infer")

app = fastapi.FastAPI(title="Chater")
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
    llama_template =f"""<s>[INST]<<SYS>>You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. \
    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.<</SYS>>{prompt}\n[/INST]"""
    return llama_template

def inference(message, history):
    prompt = format_prompt(message)
    partial_message = ""
    for token in client.text_generation(prompt, max_new_tokens=560, stream=True):
        partial_message += token
        yield partial_message


io = gr.ChatInterface(
    inference,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Chat with me!", container=False, scale=7),
    description="This is the demo for Gradio UI consuming TGI endpoint with Llama-2-7B-32K-Instruct-GPTQ model.",
    title="Gradio 🤝 TGI",
    examples=["Are tomatoes vegetables?"],
    retry_btn="Retry",
    undo_btn="Undo",
    clear_btn="Clear",
)

if __name__ == "__main__":
   demo = gr.mount_gradio_app(app, io, path='/')  
   uvicorn.run(app, host="0.0.0.0", port=8003, workers=1)