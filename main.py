from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
import json
import uuid
import httpx
import asyncio
import requests

app = FastAPI()

COMFYUI_BASE_URL = "http://127.0.0.1:8188"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(upload_file):
    filename = f"{uuid.uuid4().hex}_{upload_file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return filename

def upload_image_to_server(filename):
    with open(f"uploads/{filename}", "rb") as f:
        files = {"image": f}
        response = requests.post(f"{COMFYUI_BASE_URL}/upload/image", files=files)
    return response

def load_workflow_template():
    with open("workflow_template.json") as f:
        return f.read()

def fill_workflow_template(image1_filename, image2_filename, clothes_type, body_type):
    return load_workflow_template() \
        .replace("{image1}", image1_filename) \
        .replace("{image2}", image2_filename) \
        .replace("{clothes_type}", clothes_type) \
        .replace("{prompt_text}", body_type_prompt().get(body_type, ""))

def body_type_prompt():
    return {
        "Emaciated": "an emaciated woman, standing, facing front, white background, full body, visible bones, bony arms, neutral pose, soft lighting, photorealistic, DSLR shot",
        "Slim": "a slim woman, standing, facing forward, white background, full body, delicate build, minimalistic background, natural lighting, 4k photo, fashion model pose",
        "Overweight": "a chubby woman, standing, facing forward, white background, soft curves, full body, neutral pose, realistic body shape, 4k DSLR photo",
        "Obese": "an obese woman, standing, facing forward, plain white background, very large body, full body shot, neutral expression, studio lighting, realistic DSLR photo",
        "Average": "an average build woman, full body, standing, facing front, plain white background, simple lighting, realistic body proportions, casual appearance, DSLR photo"
    }

async def post_prompt(workflow_json):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{COMFYUI_BASE_URL}/prompt", json=workflow_json)
    
    if res.status_code != 200:
        raise Exception(res.text)
    
    return res.json()["prompt_id"]


async def check_progress(prompt_id):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{COMFYUI_BASE_URL}/history/{prompt_id}")
    
    if res.status_code != 200:
        raise Exception(f"ComfyUI 응답 오류 - 상태코드 {res.status_code}")

    return res.json()

@app.post("/generate")
async def generate_image(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    clothes_type: str = Form(...),
    body_type: str = Form(...)
):
    image1_filename = save_file(image1)
    image2_filename = save_file(image2)

    upload_image_to_server(image1_filename)
    upload_image_to_server(image2_filename)

    prompt = fill_workflow_template(image1_filename, image2_filename, clothes_type, body_type)
    workflow_json = { "prompt": json.loads(prompt) }

    try:
        prompt_id = await post_prompt(workflow_json)

        async def stream():
            yield f"{prompt_id} 생성 요청"

            for i in range(300):
                await asyncio.sleep(1)

                yield f"{prompt_id} 생성 중입니다... 진행시간 {i+1}sec"

                try:
                    data = await check_progress(prompt_id)

                    if prompt_id in data and "outputs" in data[prompt_id]:
                        last_output = list(data[prompt_id]["outputs"].values())[-1]
                        last_image = last_output["images"][-1]

                        url = f"{COMFYUI_BASE_URL}/api/view?filename={last_image['filename']}&type={last_image['type']}&subfolder={last_image['subfolder']}"
                        yield f"data: <img src='{url}'>"
                        
                        return
                except Exception as e:
                    yield f"🔴 요청 실패 - {str(e)}"
            yield "❌ 시간 초과 또는 실패"

        return StreamingResponse(stream(), media_type="text/event-stream")
    except Exception as e:
        return {"error": str(e)}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
