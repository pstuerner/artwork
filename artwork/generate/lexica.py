import httpx
import random
import string
import uuid
import re

class Lexica:
    def __init__(self, query, negativePrompt="", guidanceScale: int = 7, width: int = 768, height: int = 1152, model: str = "lexica-aperture-v3", cookie=None):
        self.query = query
        self.negativePrompt = negativePrompt
        self.guidanceScale = guidanceScale
        self.width = width
        self.height = height
        self.model = model
        self.cookie = cookie

    def images(self):
        response = httpx.post("https://lexica.art/api/infinite-prompts", json={
            "text": self.query,
            "searchMode": "images",
            "source": "search",
            "model": "lexica-aperture-v2"
        })

        prompts = [f"https://image.lexica.art/full_jpg/{ids['id']}" for ids in response.json()["images"]]

        return prompts

    def _generate_random_string(self, length):
        chars = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(chars) for _ in range(length))

        return result_str

    def generate(self):
        response = httpx.post("https://z.lexica.art/api/generator", headers={
            "cookie": self.cookie
        }, json={
            "requestId": str(uuid.uuid4()),
            "id": self._generate_random_string(20),
            "prompt": self.query,
            "negativePrompt": self.negativePrompt,
            "guidanceScale": self.guidanceScale,
            "width": self.width,
            "height": self.height,
            "enableHiresFix": False,
            "model": self.model,
            "generateSources": []
        }, timeout=50
        )

        return [f"https://image.lexica.art/full_jpg/{ids['id']}" for ids in response.json().get("images", [])]