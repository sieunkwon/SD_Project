from PIL import Image

def crop_and_resize(img: Image.Image, target_ratio=9/19.5, target_size=(720, 1080)) -> Image.Image:
    current_ratio = img.width / img.height
    if current_ratio > target_ratio:
        target_height = img.height
        target_width = int(target_height * target_ratio)
    else:
        target_width = img.width
        target_height = int(target_width / target_ratio)

    left = (img.width - target_width) // 2
    top = (img.height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    return img.crop((left, top, right, bottom)).resize(target_size)