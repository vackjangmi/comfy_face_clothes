# app/utils/comfyui_helper.py

import httpx
import asyncio
import requests

from app.core.config import COMFYUI_BASE_URL

async def post_prompt(workflow_json):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{COMFYUI_BASE_URL}/prompt", json=workflow_json)
        res.raise_for_status()

        return res.json()["prompt_id"]

async def get_history(prompt_id):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{COMFYUI_BASE_URL}/history/{prompt_id}")
        res.raise_for_status()

        return res.json()

async def generate_image(prompt_id, timeout: int = 700):
    print(f"이미지 생성 시작: {prompt_id}")

    for i in range(timeout):
        data = await get_history(prompt_id)

        if prompt_id in data:
            yield "이미지 생성 완료"
            return

        yield f"{i + 1}초 경과, 이미지 생성 중..."
        await asyncio.sleep(1)
    raise TimeoutError("시간 초과 또는 실패")

async def get_generated_image(prompt_id):
    data = await get_history(prompt_id)

    if prompt_id not in data or "outputs" not in data[prompt_id] or not data[prompt_id]["outputs"]:
        raise RuntimeError("생성된 이미지 없음")

    outputs_dict = data[prompt_id]["outputs"]

    # 'type'이 'output'인 이미지만 필터링
    filtered = [
        (key, image)
        for key in sorted(outputs_dict.keys())
        for image in outputs_dict[key].get("images", [])
        if image.get("type") == "output"
    ]

    if not filtered:
        raise RuntimeError("생성된 이미지 없음")

    print(filtered)
    # key를 정수로 변환해서 가장 큰 key의 image를 선택
    _, image = max(filtered, key=lambda x: int(x[0]))
    return f"{COMFYUI_BASE_URL}/api/view?filename={image['filename']}&type={image['type']}&subfolder={image['subfolder']}"

def upload_image(filename):
    with open(f"uploads/{filename}", "rb") as f:
        files = {"image": f}
        response = requests.post(f"{COMFYUI_BASE_URL}/upload/image", files=files)
    return response
