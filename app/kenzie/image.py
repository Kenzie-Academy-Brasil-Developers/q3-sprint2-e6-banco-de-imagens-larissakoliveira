import os
from flask import Flask, jsonify
from flask.helpers import safe_join
from werkzeug.datastructures import FileStorage
from os import getenv
import shutil
import zipfile

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

def get_dir(item: str):

    _, _, directories = list(os.walk(item))[0]
    return directories

def get_files():
    extension_folders = []

    for item in allowed_extensions.split(','):
        extension_folders = extension_folders + get_dir(f'{files_directory}/{item}')
    
    return jsonify(extension_folders)


def list_by_extension(extension):

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


# def zip_image(query_params, directory):
#     return shutil.make_archive(f"/tmp/{query_params}", 'zip', directory) 

# def zip_file(file):
#     with zipfile.ZipFile({file}, "w", compression=zipfile.ZIP_DEFLATED) as zip_image:
#         zip_image.write({file})

