from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes import router
from comfyui_helper import COMFYUI_BASE_URL, post_prompt, generate_image, upload_image, get_generated_image
import os
import shutil
import json
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file_and_upload(upload_file):
    filename = f"{uuid.uuid4().hex}_{upload_file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

    upload_image(filename)

    return filename

def body_type_prompt():
    return {
        "Emaciated": "an emaciated woman, standing, facing front, white background, full body, visible bones, bony arms, neutral pose, soft lighting, photorealistic, DSLR shot",
        "Slim": "a slim woman, standing, facing forward, white background, full body, delicate build, minimalistic background, natural lighting, 4k photo, fashion model pose",
        "Overweight": "a chubby woman, standing, facing forward, white background, soft curves, full body, neutral pose, realistic body shape, 4k DSLR photo",
        "Obese": "an obese woman, standing, facing forward, plain white background, very large body, full body shot, neutral expression, studio lighting, realistic DSLR photo",
        "Average": "an average build woman, full body, standing, facing front, plain white background, simple lighting, realistic body proportions, casual appearance, DSLR photo"
    }

def fill_workflow_template(image1_filename, image2_filename, clothes_type, body_type):
    with open("workflow_template.json") as f:
        workflow_template = f.read()

        return workflow_template \
            .replace("{image1}", image1_filename) \
            .replace("{image2}", image2_filename) \
            .replace("{clothes_type}", clothes_type) \
            .replace("{prompt_text}", body_type_prompt().get(body_type, ""))


@app.post("/generate")
async def generate(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    clothes_type: str = Form(...),
    body_type: str = Form(...)
):
    image1_filename = save_file_and_upload(image1)
    image2_filename = save_file_and_upload(image2)

    prompt = fill_workflow_template(image1_filename, image2_filename, clothes_type, body_type)
    workflow_json = { "prompt": json.loads(prompt) }

    try:
        prompt_id = await post_prompt(workflow_json)
        print(f"prompt_id: {prompt_id}")

        async def stream():
            yield f"data: {prompt_id} 생성 중입니다..."
            print(f"prompt_id: {prompt_id}")

            try:
                async for progress in generate_image(prompt_id):
                    yield f"data: {progress}"

                image_url = await get_generated_image(prompt_id)
                yield f"data: <img src='{image_url}'>"
            except Exception as e:
                yield f"data: 🔴 요청 실패 - {str(e)}"

        return StreamingResponse(stream(), media_type="text/event-stream")
    except Exception as e:
        return {"error": str(e)}

# HTML templates 디렉토리
templates = Jinja2Templates(directory="app/templates")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

# API 라우터 등록
app.include_router(router)