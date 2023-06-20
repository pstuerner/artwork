import io
import typer
import requests

from PIL import Image
from datetime import datetime as dt
from artwork.generate.chat import generate_essay
from artwork.generate.lexica import Lexica
from artwork.db.mongo import db
from artwork.data import path_data
from artwork.bot.twitter import clientV1, clientV2

app = typer.Typer()


@app.command()
def generate(
        date: str = typer.Option(default=None)
    ):
    if date:
        date = dt.strptime(date, "%Y%m%d")
    else:
        now = dt.now()
        date = dt(now.year, now.month, now.day)

    dt_str = date.strftime("%Y%m%d")
    dt_start = dt.strptime(f"{date.year} {date.isocalendar().week} 1", "%Y %W %w")
    campaign = db.timetable.find_one({"date":dt_start})
    name = campaign["data"][dt_str]
    artwork_exists = db.artwork.count_documents({"date":date}) > 0
    image_paths = []

    if not artwork_exists:
        essay = generate_essay(campaign["prompt"]["essay"].format(name=name))
        
        cookies = db.config.find_one({"name":"lexica"})["cookies"]
        urls = Lexica(
            query=campaign["prompt"]["artwork"].format(name=name),
            width=campaign["width"],
            height=campaign["height"],
            model="lexica-aperture-v3",
            cookie=cookies[0] if now.day <= 15 else cookies[1]
        ).generate()

        images = {
            1: [],
            0.5: [],
            0.25: [],
            0.125: [],
            0.02: []
        }
        
        for i, url in enumerate(urls):
            im = Image.open(requests.get(url, stream=True).raw)
            im.save(path_data / "temp" / f"{i}.jpg")
            image_paths.append(path_data / "temp" / f"{i}.jpg")

            for res in [1, 0.5, 0.25, 0.125, 0.02]:
                image_bytes = io.BytesIO()
                im_resize = im.resize([int(res * s) for s in im.size]) if res != 1 else im
                im_resize.save(image_bytes, format='JPEG')

                images[res].append(image_bytes.getvalue())

        db.artwork.insert_one(
            {
                "date": date,
                "topic": campaign["topic"],
                "name": name,
                "essay": essay,
                "prompt": campaign["prompt"]["artwork"].format(name=name),
                "images_100": images[1],
                "images_050": images[0.5],
                "images_025": images[0.25],
                "images_0125": images[0.125],
                "images_002": images[0.02],
            }
        )
    else:
        artwork = db.artwork.find_one({"date":date})
        essay = artwork["essay"]
        
        for i, image_bytes in enumerate(artwork["images_100"]):
            im = Image.open(io.BytesIO(image_bytes))
            im.save(path_data / "temp" / f"{i}.jpg")
            image_paths.append(path_data / "temp" / f"{i}.jpg")

    media_ids = []
    for image_path in image_paths:
        media = clientV1.media_upload(image_path)
        media_ids.append(media.media_id_string)
    
    text_url = f"\n👀🔗https://philippstuerner.com/e/{date.year}/{date.month}/{date.day}"
    available_length = 240 - len(text_url)
    text_body = essay.replace(name,f"#{name.replace(' ','')}")[:available_length-3]+"..."
    
    clientV2.create_tweet(
        text = text_body + text_url,
        media_ids = media_ids
    )

    
@app.command()
def dummy():
    return {}

def main():
    app()

if __name__ == "__main__":
    main()