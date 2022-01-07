import os
from flask.helpers import safe_join
from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone
from os import getenv

files_directory = getenv('FILES_DIRECTORY')
allowed_extensions = getenv('ALLOWED_EXTENSIONS')

def save_image(file: FileStorage, file_extension: str):
    filename = file.filename.split('.')[0]
    filename = f'{filename}.{file_extension}'
    if file_extension == 'jpg':
        path = safe_join(f'{files_directory}/jpg/{filename}')
        file.save(path)
    if file_extension == 'gif':
        path = safe_join(f'{files_directory}/gif/{filename}')
        file.save(path)
    if file_extension == 'png':
        path = safe_join(f'{files_directory}/png/{filename}')
        file.save(path)

    return filename


def list_all(extension):

    list_all_images = []
    files_list = os.listdir(f'{files_directory}/{extension}')

    if extension == 'jpg':
        list_all_images.append(files_list)
        return files_list

    if extension == 'png':
        list_all_images.append(files_list)
        return files_list

    if extension == 'gif':
        list_all_images.append(files_list)
        return files_list

    return list_all_images


def get_path(filename: str, extension: str):
    path = safe_join(files_directory,extension,filename)

    return path

def zip_images():
    ...