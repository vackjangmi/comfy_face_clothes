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

mkdir -p models/checkpoints models/ipadapter models/clip_vision models/lora models/controlnet models/ultralytics/bbox models/sams

curl -L "https://huggingface.co/lllyasviel/fav_models/resolve/main/fav/realisticVisionV51_v51VAE.safetensors?download=true" -o models/checkpoints/realisticVisionV51_v51VAE.safetensors
curl -L "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15.bin?download=true" -o models/ipadapter/ip-adapter-faceid-plusv2_sd15.bin
curl -L "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors?download=true" -o models/ipadapter/ip-adapter-plus_sd15.safetensors
curl -L "https://huggingface.co/Kuvshin/models-moved/resolve/main/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors?download=true" -o models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors
curl -L "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15_lora.safetensors?download=true" -o models/lora/ip-adapter-faceid-plusv2_sd15_lora.safetensors
curl -L "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth?download=true" -o models/controlnet/control_v11p_sd15_openpose.pth
curl -L "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt?download=true" -o models/ultralytics/bbox/face_yolov8m.pt
curl -L "https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/sams/sam_vit_b_01ec64.pth?download=true" -o models/sams/sam_vit_b_01ec64.pth
curl -L "https://huggingface.co/HCMUE-Research/SAM-vit-h/resolve/main/sam_vit_h_4b8939.pth?download=true" -o models/sams/sam_vit_h_4b8939.pth

#python main.py