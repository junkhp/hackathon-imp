FROM nh122112/cyclegan-pix2pix:1.0

RUN apt-get -y update \
    && apt-get install -y git zip unzip \
    libgl1-mesa-dev libglib2.0-0 libsm6 libxrender1 libxext6 gcc

RUN cd /workspace \
    && git clone https://github.com/pepepor123/hackathon-imp.git \
    && cd ./hackathon-imp \
    && git pull origin develop:develop \
    && git checkout develop \
    && pip install -r requirements.txt \
    && mkdir ./rm_mask/inpainting/weights \
    && wget https://www.dropbox.com/s/30luxykt3jfrzlx/weights.zip?dl=0 -O ./rm_mask/inpainting/weights/weights.zip \
    && cd ./rm_mask/inpainting/weights/ \
    && unzip ./weights.zip \
    && cd /workspace/hackathon-imp/rm_mask/estimate_mask_edge_positions/RetinaFaceAntiCov/rcnn/cython \
    && python setup.py build_ext --inplace

CMD ["/bin/bash"]
