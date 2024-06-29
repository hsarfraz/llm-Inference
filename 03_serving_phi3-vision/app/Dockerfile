FROM nvcr.io/nvidia/pytorch:24.03-py3

USER root
#--------------------------------------------------------------------------------
# upload easyocr model and sentence transformer model insider docker container
# latin_g2, english_g2 & craft_mlt_25k
#--------------------------------------------------------------------------------

# ADD EasyOCR/model/. /EasyOCR/model
# ADD sentence_similarity_spanish_es/. /sentence_similarity_spanish_es

COPY serve_phi_fastapi.py /workspace/
# COPY funcs.py /workspace/
# COPY root.json /workspace/
COPY req.txt .
#COPY admin_panel/ /workspace/admin_panel/
#COPY client_panel/ /workspace/client_panel/

# RUN set -xe \
#    && apt-get update \
#    # && apt-get install -y gcc default-libmysqlclient-dev pkg-config build-essential\
#    && apt-get install -y python3-pip
RUN pip3 install -r req.txt

#execute 
CMD ["python3", "/workspace/serve_phi_fastapi.py"]