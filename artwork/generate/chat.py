import openai
from artwork.utils import API_KEY

openai.api_key = API_KEY

def generate_essay(
        prompt_essay
):
    essay_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": prompt_essay},
            ]
    )

    return essay_response['choices'][0]['message']['content']
    

def generate_essay_and_artwork(
        prompt_essay,
        prompt_artwork
    ):
    essay_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": prompt_essay},
            ]
    )

    essay = essay_response['choices'][0]['message']['content']

    artwork_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": prompt_essay},
                {"role": "assistant", "content": essay},
                {"role": "user", "content": prompt_artwork},
            ]
    )

    artwork = artwork_response['choices'][0]['message']['content']

    return {
        "essay": essay,
        "title": artwork[len("Title: "):artwork.find(", Description: ")],
        "description": artwork[artwork.find("Description: ")+len("Description: "):]
    }