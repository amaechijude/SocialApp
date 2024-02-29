from PIL import Image

def compress_image(image_data):
    image = Image.open(image_data)
    image = image.resize((300, 300))
    image = image.save(image_data, quality=80)

    return image
