from dota2api.src.parse import GetById
from settings import get_full_path
import requests
import os

getById = GetById()
hero_path = get_full_path('images', 'heroes')
heroes = getById.heroes

item_path = get_full_path('images', 'items')
items = getById.items


def save_collection_of_images(collection: dict, path: str, key_of_image: str):
    for key, value in collection.items():
        url = value[key_of_image]
        r = requests.get(url)

        with open(os.path.join(path, key) + '.jpg', 'wb') as f:
            f.write(r.content)


save_collection_of_images(heroes, hero_path, "url_large_portrait")
save_collection_of_images(items, item_path, "url_image")
