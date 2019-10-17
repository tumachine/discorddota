from bs4 import BeautifulSoup
import requests
import os

# source = requests.get('https://dota2.gamepedia.com/Matchmaking/Seasonal_Rankings').content
with open(r'C:\Users\Tumen\Desktop\Matchmaking_Seasonal Rankings - Dota 2 Wiki.html', 'r') as f:
    source = f.read()

# C:\Users\Tumen\Desktop\Matchmaking_Seasonal Rankings - Dota 2 Wiki.html
soup = BeautifulSoup(source, 'html.parser')
# <span class="priceText__1853e8a5">2,732.11</span>

rank_image_links = []
rank_names = []

def fill_ranks():
    for rank_list in soup.find_all(attrs={'class': 'ranks'}):
        for ranks in rank_list.find_all('a', attrs={'class': 'image'}):
            rank_img = ranks.img
            rank_names.append(rank_img['alt'].replace('SeasonalRank', ''))
            rank_image_links.append(rank_img['src'])
            print(rank_img)


ranks_folder_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'ranks'))
print(ranks_folder_path)
fill_ranks()
for i in range(len(rank_names)):
    rank_name = rank_names[i]
    rank_link = rank_image_links[i]
    r = requests.get(rank_link)

    with open(os.path.join(ranks_folder_path, rank_name), 'wb') as f:
        f.write(r.content)
print('a')