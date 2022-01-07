import os
from flask import Flask, jsonify
from flask.helpers import safe_join
from werkzeug.datastructures import FileStorage
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


def get_files():
    extension_folders = []
    directory = os.walk(f'./{files_directory}')

    for _,_,each in directory:
        extension_folders.append(each)

    return jsonify(
        jpg=extension_folders[0],
        gif=extension_folders[1],
        png=extension_folders[2]
    )


def list_by_extension(extension):

    list_all_images = list()

    # for extent in allowed_extensions:
    #     final_dir = os.listdir(f'{files_directory}/{extent}
    #     list_all_images.append(final_dir)

    files_list = os.listdir(f'{files_directory}/{extension}')

    if extension == 'jpg':
        return files_list

    if extension == 'png':
        return files_list

    if extension == 'gif':
        return files_list



def get_path(filename: str, extension: str):
    path = safe_join(files_directory,extension,filename)

    return path


def zip_images():
    ...