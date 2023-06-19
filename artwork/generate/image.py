import openai
from artwork.utils import API_KEY
from artwork.db.mongo import db
from artwork.generate.lexica import Lexica

openai.api_key = API_KEY

def generate_image(description):
    image = openai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024"
    )

    return image['data'][0]['url']
