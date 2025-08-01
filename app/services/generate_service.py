# app/services/generate_service.py

import json
import uuid
import shutil
import os

from fastapi.responses import StreamingResponse

from app.core.config import UPLOAD_DIR, WORKFLOW_DIR
from app.utils.comfyui_helper import post_prompt, generate_image, upload_image, get_generated_image
from app.utils.seed_helper import get_random_seed

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
        "female": {
            "Emaciated": "(an emaciated woman:1.5), standing, facing front, white background, full body, visible bones, bony arms, neutral pose, photorealistic, DSLR shot, realistic proportions, facing front, soft lighting, standing pose, natural stance, neutral pose, natural lighting, friendly face",
            "Slim": "(a slim woman:1.5), standing, facing forward, white background, full body, delicate build, minimalistic background, natural lighting, 4k photo, fashion model pose, realistic proportions, facing front, soft lighting, standing pose, natural stance, neutral pose, natural lighting, friendly face",
            "Overweight": "(a chubby woman:1.5), standing, facing forward, white background, soft curves, full body, neutral pose, realistic body shape, 4k DSLR photo, realistic proportions, facing front, soft lighting, standing pose, natural stance, neutral pose, natural lighting, friendly face",
            "Obese": "(an obese woman:1.5), standing, facing forward, plain white background, very large body, full body shot, neutral expression, studio lighting, realistic DSLR photo, realistic proportions, facing front, soft lighting, standing pose, natural stance, neutral pose, natural lighting, friendly face",
            "Average": "(an average build woman:1.5), full body, standing, facing front, plain white background, simple lighting, realistic body proportions, casual appearance, DSLR photo, realistic proportions, facing front, soft lighting, standing pose, natural stance, neutral pose, natural lighting, friendly face"
        },
        "male": {
            "Emaciated": "(emaciated man:1.5), very thin, bony figure, visible ribs, bony arms, realistic body proportions, casual appearance, standing pose, natural stance, neutral pose, natural lighting, soft lighting, photorealistic, facing front",
            "Slim": "(slim man:1.5), thin build, delicate frame, lightweight figure, bony arms, realistic body proportions, casual appearance, standing pose, natural stance, neutral pose, natural lighting, soft lighting, photorealistic, facing front",
            "Average": "(average build man:1.5), fit body, healthy body type, normal physique, bony arms, realistic body proportions, casual appearance, standing pose, natural stance, neutral pose, natural lighting, soft lighting, photorealistic, facing front",
            "Overweight": "(overweight man:1.5), heavyset, bigger figure, round body shape, bony arms, realistic body proportions, casual appearance, standing pose, natural stance, neutral pose, natural lighting, soft lighting, photorealistic, facing front",
            "Obese": "(obese man:1.5), morbidly obese, extremely large body, massive figure, bony arms, realistic body proportions, casual appearance, standing pose, natural stance, neutral pose, natural lighting, soft lighting, photorealistic, facing front"
        }
    }
    

def fill_workflow_template(image1_filename, image2_filename, image3_filename, input_mode, clothes_type1, clothes_type2, human_info, gender, body_type):

    workflow_file = "new_workflow_single_template.json" if input_mode == "1" else "new_workflow_multiple_template.json"
    workflow_path = os.path.join(os.path.dirname(__file__), f"../../{WORKFLOW_DIR}/{workflow_file}")
    workflow_path = os.path.abspath(workflow_path)

    with open(workflow_path) as f:
        workflow_template = f.read()

        return workflow_template \
            .replace("{image1}", image1_filename) \
            .replace("{image2}", image2_filename) \
            .replace("{image3}", image3_filename) \
            .replace("{seed1}", str(get_random_seed())) \
            .replace("{seed2}", str(get_random_seed())) \
            .replace("{seed3}", str(get_random_seed())) \
            .replace("{seed4}", str(get_random_seed())) \
            .replace("{seed5}", str(get_random_seed())) \
            .replace("{clothes_type1}", clothes_type1) \
            .replace("{clothes_type2}", clothes_type2) \
            .replace("{human_info}", human_info) \
            .replace("{prompt_text}", body_type_prompt().get(gender).get(body_type, ""))

async def process_generate(image1, image2, image3, input_mode, clothes_type1, clothes_type2, gender, body_type):
    image1_filename = save_file_and_upload(image1)
    image2_filename = save_file_and_upload(image2)
    image3_filename = save_file_and_upload(image3)

    human_info = ""

    prompt = fill_workflow_template(image1_filename, image2_filename, image3_filename, input_mode, clothes_type1, clothes_type2, human_info, gender, body_type)
    workflow_json = { "prompt": json.loads(prompt) }

    prompt_id = await post_prompt(workflow_json)

    async def stream():
        yield f"data: {prompt_id} 생성 중입니다..."
        async for progress in generate_image(prompt_id):
            yield f"data: {progress}"
        image_url = await get_generated_image(prompt_id)
        yield f"data: <img src='{image_url}'>"

    return StreamingResponse(stream(), media_type="text/event-stream")
