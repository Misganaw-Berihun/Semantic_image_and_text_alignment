from PIL import Image
import os

def get_image_dimensions(image_path: str) -> tuple:
   
    with Image.open(image_path) as img:
        width, height = img.size

    return width, height

def resize_and_save_image(image_path: str, new_width: int, new_height: int, output_dir: str = '../images/resized_images') -> None:
   
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, filename)

    with Image.open(image_path) as img:
        resized_img = img.resize((new_width, new_height))
        resized_img.save(output_path)

    print(f"Resized image saved to {output_path}")
