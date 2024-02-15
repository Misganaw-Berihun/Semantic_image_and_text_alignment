import os
import logging
from typing import Literal,List,Tuple,Optional,Dict
import base64
from dotenv import load_dotenv
from io import BytesIO

import requests
import replicate
from PIL import Image
import requests
from pydantic import HttpUrl
from http.client import HTTPResponse

load_dotenv()

os.environ["REPLICATE_API_TOKEN"] = 'r8_0gtYm4UC2kwFP09VIDyrCl0hqEdo4Qf1lyvPd'
logging.basicConfig(level=logging.INFO)

class ImageGenerator:
    def __init__(self, asset_suggestions: dict) -> None:
        self.asset_suggestions = asset_suggestions
    def generate_images(self, store_location: str = '../images') -> Dict[str, List[Tuple[str, str]]]:
        keyType = str
        valueType = List[Tuple[str,str]]
        generated_images:Dict[keyType, valueType] = {}
        for frame, elements in self.asset_suggestions.items():
            if frame.startswith('frame'):
                generated_images[frame] = []
                for type, description in elements.items():
                    try:
                        # Generate image
                        generated_image_path = ImageGenerator.download_image(ImageGenerator.generate_image(prompt=description)[0], store_location)
                        # Append generated image path to the list
                        generated_images[frame].append((type, *generated_image_path))
                    except Exception as e:
                        print(f"An error occurred while generating image: {e}")
        return generated_images
    @staticmethod
    def generate_image(prompt: str, performance_selection: Literal['Speed', 'Quality', 'Extreme Speed'] = "Extreme Speed", 
                       aspect_ratios_selection: str = "1024*1024", image_seed: int = 1234, sharpness: int = 2) -> Optional[dict]:
        """
        Generates an image based on the given prompt and settings.

        :param prompt: Textual description of the image to generate.
        :param performance_selection: Choice of performance level affecting generation speed and quality.
        :param aspect_ratio: The desired aspect ratio of the generated image.
        :param image_seed: Seed for the image generation process for reproducibility.
        :param sharpness: The sharpness level of the generated image.
        :return: The generated image or None if an error occurred.
        """
        try:
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": prompt,
                    "performance_selection": performance_selection,
                    "aspect_ratios_selection": aspect_ratios_selection,
                    "image_seed": image_seed,
                    "sharpness": sharpness
                }
            )
            
            logging.info("Image generated successfully.")
            return output
        except Exception as e:
            logging.error(f"Failed to generate image: {e}")
            return None
    @staticmethod
    def decode_image(base64_data: str) -> Optional[Image.Image]:
        try:
            # Decode base64 image data
            image_data = base64.b64decode(base64_data)
            # Create a BytesIO stream from the decoded data
            image_stream = BytesIO(image_data)
            # Open the image from the stream
            image = Image.open(image_stream)
            return image
        except Exception as e:
            print(f"An error occurred while decoding the image: {e}")
            return None
    @staticmethod 
    def download_image(url: str, save_path: str) -> Tuple[str, str]:
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                # Extract filename from URL
                filename = os.path.basename(url)
                # Join save_path and filename to form complete path
                complete_path = os.path.join(save_path, filename)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(complete_path), exist_ok=True)
                
                # Open image
                image = Image.open(BytesIO(response.content))
                # Save image with specified format
                image.save(complete_path, format=image.format)
                logging.info(f"Image saved to {complete_path}")
                return (url, complete_path)
            else:
                raise RuntimeError(f"Failed to download image. Status code: {response.status_code}")
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}") from e
        
if __name__ =='__main__':
    a = {
    "frame_1": {
        "Animated Element": "A high-resolution 3D Coca-Cola bottle center-screen, bubbles rising to the top, transitioning into a sleek DJ turntable with a vinyl record that has the Coke Studio logo.",
    },
    "frame_2": {
        "CTA Text": "'Mix Your Beat' in bold, playful font pulsating to the rhythm of a subtle background beat, positioned at the bottom of the screen."
    },
    "explanation": "This variation emphasizes the joy and interactivity of music mixing, with each frame building on the last to create a crescendo of engagement. The 3D bottle-to-turntable animation captures attention, the interactive beat mixer sustains engagement, and the vibrant animations encourage sharing, aligning with the campaign's objectives of engagement and message recall."
    }
    test = ImageGenerator(a)

    test.generate_images()
