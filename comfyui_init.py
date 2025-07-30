import os
import subprocess
import urllib.request
import ssl

# ComfyUI 클론
def clone_repo(url, dest=None):
    cmd = ["git", "clone", url]
    if dest:
        cmd.append(dest)
    subprocess.run(cmd, check=True)

def pip_install(packages):
    if isinstance(packages, str):
        packages = [packages]
    subprocess.run(["pip", "install"] + packages, check=True)

def pip_install_in_comfyui(packages):
    if isinstance(packages, str):
        packages = [packages]
    subprocess.run(["pip", "install", "-r", "requirements.txt"] if packages == ["-r", "requirements.txt"] else ["pip", "install"] + packages, check=True, cwd="ComfyUI")

def download_file_in_comfyui(url, dest):
    print(f"Downloading {url} to {dest}")
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, dest)

# 1. ComfyUI 클론 (이미 존재하면 생략)
if os.path.exists("ComfyUI"):
    print("이미 존재: ComfyUI, git clone 생략")
else:
    git_url = "https://github.com/comfyanonymous/ComfyUI"
    clone_repo(git_url)

# 2. requirements.txt 및 pip 패키지 설치
pip_install_in_comfyui(["-r", "requirements.txt"])
pip_install_in_comfyui("insightface")
pip_install_in_comfyui(["onnxruntime", "onnx", "numpy"])

# 3. custom_nodes 클론
custom_nodes = [
    ("https://github.com/ltdrdata/ComfyUI-Manager", "ComfyUI/custom_nodes/comfyui-manager"),
    ("https://github.com/cubiq/ComfyUI_IPAdapter_plus", "ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus"),
    ("https://github.com/Fannovel16/comfyui_controlnet_aux", "ComfyUI/custom_nodes/comfyui_controlnet_aux"),
    ("https://github.com/ltdrdata/ComfyUI-Impact-Pack", "ComfyUI/custom_nodes/ComfyUI-Impact-Pack"),
    ("https://github.com/kijai/ComfyUI-Florence2", "ComfyUI/custom_nodes/ComfyUI-Florence2"),
    ("https://github.com/storyicon/comfyui_segment_anything", "ComfyUI/custom_nodes/comfyui_segment_anything"),
    ("https://github.com/cubiq/ComfyUI_essentials", "ComfyUI/custom_nodes/ComfyUI_essentials"),
    ("https://github.com/Nourepide/ComfyUI-Allor", "ComfyUI/custom_nodes/ComfyUI-Allor"),
    ("https://github.com/ltdrdata/ComfyUI-Impact-Subpack", "ComfyUI/custom_nodes/ComfyUI-Impact-Subpack"),
    ("https://github.com/ltdrdata/was-node-suite-comfyui", "ComfyUI/custom_nodes/was-node-suite-comfyui"),
    ("https://github.com/ai-shizuka/ComfyUI-tbox", "ComfyUI/custom_nodes/ComfyUI-tbox"),
]
for url, dest in custom_nodes:
    if os.path.exists(dest):
        print(f"이미 존재: {dest}, git clone 생략")
        continue
    clone_repo(url, dest)

# 4. pip 패키지 추가 설치
pip_packages = [
    "segment-anything",
    "scikit-image>=0.20.0",
    "piexif",
    "opencv-python-headless",
    "scipy>=1.11.4",
    "numpy",
    "dill",
    "matplotlib",
    "git+https://github.com/facebookresearch/sam2",
    "segment_anything",
    "timm>=0.4.12",
    "addict",
    "yapf",
    "rembg",
    "ultralytics>=8.3.162",
    "cmake",
    "fairscale>=0.4.4",
    "git+https://github.com/ltdrdata/img2texture.git",
    "git+https://github.com/ltdrdata/cstr",
    "imageio",
    "joblib",
    "numba",
    "pilgram",
    "git+https://github.com/ltdrdata/ffmpy.git",
    "scikit-learn",
    "tqdm",
    "transformers==4.49.0",
]
for pkg in pip_packages:
    pip_install_in_comfyui(pkg)

# 5. 모델 디렉토리 생성
model_dirs = [
    "models/checkpoints",
    "models/ipadapter",
    "models/clip_vision",
    "models/lora",
    "models/controlnet",
    "models/ultralytics/bbox",
    "models/sams",
]
for d in model_dirs:
    os.makedirs(os.path.join("ComfyUI", d), exist_ok=True)

# 6. 모델 파일 다운로드
model_downloads = [
    ("https://huggingface.co/lllyasviel/fav_models/resolve/main/fav/realisticVisionV51_v51VAE.safetensors?download=true", "ComfyUI/models/checkpoints/realisticVisionV51_v51VAE.safetensors"),
    ("https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15.bin?download=true", "ComfyUI/models/ipadapter/ip-adapter-faceid-plusv2_sd15.bin"),
    ("https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors?download=true", "ComfyUI/models/ipadapter/ip-adapter-plus_sd15.safetensors"),
    ("https://huggingface.co/Kuvshin/models-moved/resolve/main/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors?download=true", "ComfyUI/models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"),
    ("https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15_lora.safetensors?download=true", "ComfyUI/models/loras/ip-adapter-faceid-plusv2_sd15_lora.safetensors"),
    ("https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth?download=true", "ComfyUI/models/controlnet/control_v11p_sd15_openpose.pth"),
    ("https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt?download=true", "ComfyUI/models/ultralytics/bbox/face_yolov8m.pt"),
    ("https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/sams/sam_vit_b_01ec64.pth?download=true", "ComfyUI/models/sams/sam_vit_b_01ec64.pth"),
    ("https://huggingface.co/HCMUE-Research/SAM-vit-h/resolve/main/sam_vit_h_4b8939.pth?download=true", "ComfyUI/models/sams/sam_vit_h_4b8939.pth"),
]
for url, dest in model_downloads:
    if os.path.exists(dest):
        print(f"이미 존재: {dest}, 다운로드 생략")
        continue
    print(f"Downloading {url} to {dest}")
    urllib.request.urlretrieve(url, dest)

# 7. (선택) ComfyUI 실행
# subprocess.run(["python", "main.py"], cwd="ComfyUI")
