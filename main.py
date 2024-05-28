from openai import OpenAI
from dotenv import load_dotenv

import requests
import os
import subprocess

from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_image(prompt):
    response = client.images.generate(prompt=prompt,
    n=1,
    size="1024x1024")
    image_url = response.data[0].url
    return image_url

def save_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_name = f"wallpaper_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        with open(image_name, 'wb') as f:
            f.write(response.content)
        return image_name
    else:
        return None

def set_wallpaper(image_path):
    script = f"""
    osascript -e 'tell application "System Events" to set picture of every desktop to "{os.path.abspath(image_path)}"'
    """
    subprocess.run(script, shell=True, check=True)

if __name__ == "__main__":
    prompt = "Create a desktop wallpaper."
    image_url = generate_image(prompt)
    if image_url:
        image_name = save_image(image_url)
        if image_name:
            set_wallpaper(image_name)
            print(f"Wallpaper set to {image_name}")
        else:
            print("Failed to save image")
    else:
        print("Failed to generate image")