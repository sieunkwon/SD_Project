from diffusers import StableDiffusionPipeline
import torch
from core.image_utils import crop_and_resize
from core.config import system_prompt, negative_prompt


model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16
)
pipe.to("cuda")
# 성능 최적화
pipe.enable_attention_slicing()

def generate_images(user_prompt: str, public_url: str):
    full_prompt = system_prompt + user_prompt
    images = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        height=1024,
        width=1024,
        guidance_scale=7.5,
        num_inference_steps=30,
        num_images_per_prompt=2
    ).images

    image_urls = []
    for i, img in enumerate(images):
        processed = crop_and_resize(img)
        filename = f"generated_image_{i}.png"
        processed.save(filename)
        image_urls.append(f"{public_url}/image/{i}")
    return image_urls
