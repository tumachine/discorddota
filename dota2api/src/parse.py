#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse some of the values from the API, all can be found in the ``response`` returned"""

import json
import os
from .urls import BASE_ITEMS_IMAGES_URL, BASE_HERO_IMAGES_URL
from utils.util import get_full_path


def load_json_file(file_name):
    return get_full_path('dota2api', 'ref', file_name)


class GetById:
    def __init__(self):
        with open(load_json_file("heroes.json")) as heroes_json:
            self.heroes = json.load(heroes_json)
        with open(load_json_file("items.json")) as items_json:
            self.items = json.load(items_json)
        with open(load_json_file("mode.json")) as modes_json:
            self.modes = json.load(modes_json)
        with open(load_json_file("region.json")) as regions_json:
            self.regions = json.load(regions_json)
        with open(load_json_file("cluster.json")) as clusters_json:
            self.clusters = json.load(clusters_json)
        with open(load_json_file("leaver.json")) as leaver_json:
            self.leavers = json.load(leaver_json)
        with open(load_json_file('lobby.json')) as lobbies_json:
            self.lobbies = json.load(lobbies_json)

    def get_hero_id_by_name(self, hero_name) -> int:
        for key, val in self.heroes.items():
            if val['localized_name'].lower() == hero_name.lower():
                return int(key)
        return -1

    def get_region_name_by_cluster_id(self, cluster_id):
        return self.regions[str(self.clusters[str(cluster_id)]['regionId'])]['clientName']


def parse_items_images_urls(resp):
    for item in resp['items']:
        item['url_image'] = BASE_ITEMS_IMAGES_URL + item['name'].replace('item_', '') + '_lg.png'


def parse_heroes_images(resp):
    for hero in resp['heroes']:
        base_images_url = BASE_HERO_IMAGES_URL + hero['name'].replace('npc_dota_hero_', '')

        hero['url_small_portrait'] = base_images_url + '_sb.png'
        hero['url_large_portrait'] = base_images_url + '_lg.png'
        hero['url_full_portrait'] = base_images_url + '_full.png'
        hero['url_vertical_portrait'] = base_images_url + '_vert.jpg'


get_by_id = GetById()
