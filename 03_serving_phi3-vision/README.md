
# Inference using Microsoft phi3-vision model
Microsoft Phi3 vision language model is latest state-of-the art language model. This repo provides implementation of python/flask based web server to host model on premise for runtime inference. It provides examples to perform OCR and other functions using command line utilities like curl. The tiny Phi3-vision inference server is a simplified implementation to host model on premise. It is designed for small scale inference deployments with max serving capacity for 1-5 users. 

It provides a simple REST based interface to allow utilization of the model. Inference server is based on a single Docker container that provides following key capabilities: 

1. Phi-3 model Inference
2. REST APIs for integration with llm
3. Support for quantized models

## Deliverables
- REST Interface to allow interaction with Phi-3 model
- Inference server configuration and setup 

## Supported Models

| Models              | OCR  | CUDA | 
| :------------------ | -----| :--: | 
| Phi-3-vision        | yes  |  ✅  | 
| Phi-3-medium        | no   |  ✅  | 
| Phi-3-small         | no   |  ✅  | 
| Phi-3-mini          | no   |  ✅  | 

## Requirement
- Linux server with GPU and CUDA Support
- Docker 
- Pytorch, Transformers, flash-attn
- uvicorn and fastapi 

```diff
version: "3.8"
services:
  phiserv:
    build:
      context: ./app
    container_name: phiserv
    hostname: phiserv
    environment:
      MODEL: microsoft/Phi-3-vision-128k-instruct
    ports:
      - "5000:5000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]  
    volumes:
      - ./model/:/root/.cache/huggingface  

```
## Deploy 
After making the necessary updates to the [`docker-compose.yml`] (./02_tiny_inference_single_model/docker-compose.yml) file to accurately reflect your local development environment, you're now ready to build and deploy your containers. To do so, follow these steps:

1. Run docker-compose build to rebuild your containers using the updated configuration.
2. Next, execute docker-compose up -d to start your containers in detached mode, allowing them to run in the background.

By following these commands, you'll have successfully deployed your containers and be ready to start using phi3-vision via REST web services.


```bash
docker compose build

docker compose up
or
docker compose up -d
```
Given below is typical output upon successful running of phi3-vision inference server
![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/phi3_container_running.png)

Also, below docker ps command can also be used to verify if tiny inference server is up and running
```bash
docker ps 
```
```bash
http://<HOST IP ADDRESS>:5000/
```
## Usage 
To perform Optical Character Recognition (OCR) using the Phi3-vision model, use REST end point /ocr. This end point handles OCR of a single file using default prompt or custom prompt. The end point will return text of the uploaded image. Given below are few examples of calling the /ocr end point using curl. 

```bash
curl -F "file=@<replace_with_image_filename>.png" http://<host ip address>:5000/ocr
```




# Extracting Elements from Court Case Document
Phi3-vision's exceptional capabilities in optical character recognition (OCR) have been consistently demonstrated through its impressive performance on simple documents. Not only can it accurately perform OCR tasks, but it also excels at named-entity recognition, allowing users to pinpoint specific entities mentioned within the text. Moreover, Phi3-vision returns its findings in JSON format, making it an intuitive and user-friendly solution for data extraction.

To illustrate the model's capabilities, let's put it to work on a sample document from the funds dataset. By using a court case form as our test subject, we can demonstrate how Phi3-vision can extract valuable information from a scanned document with ease. Using its advanced OCR capabilities, the tool will quickly and accurately identify the text within the image, allowing us to tap into the wealth of data contained within.

![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/82491256.png)

As we analyze the results in JSON format, we'll gain insights into specific elements extracted from the scanned document, such as dates, names, and other relevant information. This powerful combination of OCR and named-entity recognition enables users to unlock hidden value from even the most complex documents, making Phi3-vision an indispensable tool for anyone working with large datasets.

## phi3-vision prompt to extract case name and court 
Curl command with custom prompt to extract court case name and associated court
```bash
curl --form file=@82491256.png --form prompt="OCR the text of the image. Extract the text of the following fields and put it in a JSON format: 'CASE NAME','COURT'" http://<host ip address>:5001/ocr
```
The output of curl command is given below:
![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/output_court_case_name_json.png)

## phi3-vision prompt to extract case name, date filed and entities 
Curl command with custom prompt to extract court case name and associated court
```bash
curl --form file=@82491256.png --form prompt="OCR the text of the image. Extract the text as JSON of the following fields and put it in a formatted JSON: 'CASE NAME','DATE FILED', LORILLARD ENTITIES" http://192.168.100.38:5001/ocr
```

![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/output_court_case_attrib_ex2.png)

While the model is able to extract the needed attributes and accurately in a JSON format, it has also appended tokens which is undesirable. These can be handled in post OCR text processing via custom code.  

Let's measure performance of Phi3-vision for the same prompt using curl's built-in timing measurement feature by simply appending output to a text file using -o option
```bash
curl --form file=@82491256.png --form prompt="OCR the text of the image. Extract the text as JSON of the following fields and put it in a formatted JSON: 'CASE NAME','DATE FILED', LORILLARD ENTITIES" http://192.168.100.38:5001/ocr -o output.json
```
It takes around three seconds to perform OCR, named-entity recognition and return results in a JSON text file

![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/output_court_case_attrib_ex2_time.png)

The contents of the output.json file are shown below:

![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/output_court_case_attrib_ex2_json.png)

## phi3-vision hallucinations and unable to parse vertical/slanted text 
So far we have extracted particular fields from the court form document. Now we will try to perform full OCR of the document and see the results. Use below curl command without specifying any custom prompt, in this case the REST service will use default prompt to perform OCR. 

```bash
curl --form file=@82491256.png http://192.168.100.38:5000/ocr
```
The results of the curl command are displayed in below image. In this case while phi3-vision model is able to accurately perform ocr of the text, it is unable to ocr vertical and slanted text, resulting in hallucinations by providing invalid results. 

As depicted in the image, when presented with horizontal text, this phi3-vision model is remarkably effective at accurately recognizing and transcribing the written words. However, as we can see, its performance drastically drops off when confronted with vertical or slanted text. In these cases, rather than providing accurate results, the model succumbs to "hallucinations," generating invalid output that bears little resemblance to the original text. This limitation highlights the need for more sophisticated approaches to handle a wider range of text orientations and font styles. For instance, consider the following example:

![image](https://github.com/hsarfraz/llm-Inference/blob/main/03_serving_phi3-vision/_images/output_court_form_full_ocr.png)

As we can see, the model has hallucinated, producing a nonsensical string that bears no relation to the original text. 

Contact me on freelancing web sites for assistance https://www.freelancer.com/u/hsarfraz76 or https://www.upwork.com/freelancers/~0178ad46e2372c8fe5 