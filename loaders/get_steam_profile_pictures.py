from bs4 import BeautifulSoup
import requests
from utils.util import get_full_path

source = requests.get('https://sguru.org/steam-profile-pictures-184px/').content

soup = BeautifulSoup(source, 'html.parser')

img_links = []


def fill_image_links():
    for i in range(136, 146):
        for image_list in soup.find_all(attrs={'id': f'gallery-{i}'}):
            for image_link in image_list.find_all(attrs={'class': 'herald-popup'}):
                img_links.append(image_link['href'])


fill_image_links()

count = 0
for image in img_links:
    r = requests.get(image)
    with open(get_full_path('images', 'steam', f'{count}.jpg'), 'wb') as f:
        f.write(r.content)
    count += 1


print('a')
