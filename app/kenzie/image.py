import os
from flask import jsonify, send_file
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


def zip_file(file_extension: str, compression_ratio: str):
    output_file = f'{file_extension}.zip'
    input_path = os.path.join(files_directory, file_extension)
    output_path_file = os.path.join('/tmp', output_file)

    command = f'zip -j -r -{compression_ratio} {output_path_file} {input_path}'

    if os.path.isfile(output_path_file):
        os.remove(output_path_file)

    os.system(command)

    return send_file(output_path_file, as_attachment=True)