import os
from utils.util import get_full_path
import json


def save_dict_to_file(json_dict, path: str):
    out_file = open(path, "w")
    json.dump(json_dict, out_file, indent=4)
    out_file.close()


def load_json_file(path: str):
    with open(path) as json_item:
        return json.load(json_item)


def convert_to_id(json_dict: dict, path_to: str):
    new_dict = {}

    for item in json_dict:
        new_dict[item['id']] = item
        dict.pop(new_dict[item['id']], 'id')
    save_dict_to_file(new_dict, path_to)


def convert_json_files(folder_to_load, folder_to_save, file_json_names):
    for file_name in file_json_names:
        json_name = file_name + '.json'
        path_from = os.path.join(folder_to_load, json_name)
        path_to = os.path.join(folder_to_save, json_name)

        json_dict = load_json_file(path_from)
        if not isinstance(json_dict, list):
            json_dict = json_dict[file_name]

        convert_to_id(json_dict, path_to)


# folder_to_load_from = get_full_path('dota2api', 'ref', 'outdated')
# folder_to_save = get_full_path('dota2api', 'ref')
#
# file_json_names = ['abilities', 'leaver', 'lobbies', 'modes', 'regions']


folder_to_load_from = get_full_path('dota2api', 'ref', 'test')
folder_to_save = get_full_path('dota2api', 'ref')

file_json_names = ['region', 'cluster']
convert_json_files(folder_to_load_from, folder_to_save, file_json_names)


