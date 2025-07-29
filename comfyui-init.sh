#!/bin/sh

git clone https://github.com/comfyanonymous/ComfyUI

cd ComfyUI

pip install -r requirements.txt
pip install insightface
pip install onnxruntime onnx numpy

cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager comfyui-manager
git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus
git clone https://github.com/Fannovel16/comfyui_controlnet_aux
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack
git clone https://github.com/kijai/ComfyUI-Florence2
git clone https://github.com/storyicon/comfyui_segment_anything
git clone https://github.com/cubiq/ComfyUI_essentials
git clone https://github.com/Nourepide/ComfyUI-Allor
git clone https://github.com/ltdrdata/ComfyUI-Impact-Subpack
git clone https://github.com/ltdrdata/was-node-suite-comfyui
git clone https://github.com/ai-shizuka/ComfyUI-tbox

cd ..

pip install segment-anything
pip install scikit-image>=0.20.0
pip install piexif
pip install opencv-python-headless
pip install scipy>=1.11.4
pip install numpy
pip install dill
pip install matplotlib
pip install git+https://github.com/facebookresearch/sam2
pip install segment_anything
pip install timm>=0.4.12
pip install addict
pip install yapf
pip install rembg
pip install ultralytics>=8.3.162
pip install cmake
pip install fairscale>=0.4.4
pip install git+https://github.com/ltdrdata/img2texture.git
pip install git+https://github.com/ltdrdata/cstr
pip install imageio
pip install joblib
pip install numba
pip install pilgram
pip install git+https://github.com/ltdrdata/ffmpy.git
pip install scikit-learn
pip install tqdm
pip install transformers==4.49.0

#python main.py