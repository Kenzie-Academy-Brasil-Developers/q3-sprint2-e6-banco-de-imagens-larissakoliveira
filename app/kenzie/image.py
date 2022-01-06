import os
from flask.helpers import safe_join
from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone
from os import getenv

files_directory = getenv('FILES_DIRECTORY')

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