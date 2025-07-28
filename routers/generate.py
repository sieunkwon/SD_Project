from fastapi import APIRouter, Request
from pydantic import BaseModel
from core.pipeline import generate_images
from fastapi.responses import FileResponse
import os

router = APIRouter()

class PromptInput(BaseModel):
    prompt: str

@router.post("/generate/")
async def generate(input_data: PromptInput, request: Request):
    image_urls = generate_images(input_data.prompt, request.app.state.public_url)
    return {"image_urls": image_urls}

@router.get("/image/{index}")
async def get_image(index: int):
    path = f"generated_image_{index}.png"
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "Image not found"}