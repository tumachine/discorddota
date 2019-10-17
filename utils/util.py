import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))


def get_full_path(*path):
    return os.path.join(PROJECT_ROOT, *path)


def replace_dict_null(original_keys: list, replace_with, dictionary: dict):
    if isinstance(replace_with, str):
        for i in range(len(original_keys)):
            if original_keys[i] not in dictionary:
                dictionary[original_keys[i]] = replace_with
        return dictionary

    for i in range(len(original_keys)):
        if original_keys[i] not in dictionary:
            dictionary[original_keys[i]] = replace_with[i]
    return dictionary



