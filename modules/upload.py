import requests

def upload_image(image_path):
    url = "https://0x0.st"
    with open(image_path, 'rb') as file:
        response = requests.post(url, files={"file": file})
    return response.text.strip()
