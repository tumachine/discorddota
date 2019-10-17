from PIL import Image
import io
import requests
from utils.util import get_full_path


def get_image(url: str):
    return Image.open(io.BytesIO(requests.get(url).content))


def get_rank_picture(rank: int):
    rank = int(rank)
    if rank < 10:
        return Image.open(get_full_path('images', 'ranks', 'not_calibrated.png'))
    if rank == 80:
        return Image.open(get_full_path('images', 'ranks', 'Top0.png'))
    rank_medal = rank // 10
    rank_stars = (rank % 10) // 2 + 1
    return Image.open(get_full_path('images', 'ranks', f'{rank_medal}-{rank_stars}.png'))


def get_item_picture(item_id: int):
    if item_id == 0:
        return None
        # return Image.open(get_full_path('images', 'items', f"279.jpg"))
    return Image.open(get_full_path('images', 'items', f"{item_id}.jpg"))
