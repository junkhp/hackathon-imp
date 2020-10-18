FROM nh122112/cyclegan-pix2pix:1.0

RUN apt-get -y update \
    && apt-get install -y git zip unzip \
    libgl1-mesa-dev libglib2.0-0 libsm6 libxrender1 libxext6 gcc

WORKDIR /workspace

RUN git clone https://github.com/pepepor123/hackathon-imp.git \
    && pip install -r ./hackathon-imp/requirements.txt

WORKDIR /workspace/hackathon-imp/rm_mask/inpainting/weights

RUN wget https://www.dropbox.com/s/30luxykt3jfrzlx/weights.zip?dl=0 -O ./weights.zip \
    && unzip ./weights.zip

WORKDIR /workspace/hackathon-imp/rm_mask/estimate_mask_edge_positions/RetinaFaceAntiCov/rcnn/cython

RUN python setup.py build_ext --inplace

WORKDIR /workspace/hackathon-imp

CMD ["/bin/bash"]
