from flask import Flask, request
from os import getenv
import os
from werkzeug.exceptions import RequestEntityTooLarge, Conflict, UnsupportedMediaType
from .kenzie import image

app = Flask(__name__)   
files_directory = getenv('FILES_DIRECTORY')
max_content_length = int(getenv('MAX_CONTENT_LENGTH'))
allowed_extensions = getenv('ALLOWED_EXTENSIONS').split(',')

app.config['MAX_CONTENT_LENGTH'] = int(max_content_length)

if not os.path.isdir(files_directory):
    os.mkdir(files_directory)
    os.system('cd {files_directory}')
    for extension in allowed_extensions:
        path = f"{files_directory}/{extension}"
        os.makedirs(path)
            
@app.post("/upload")
def post_file(): 
    files_list = []
    
    try:
        for file in request.files:
            file_extension = request.files[file].filename.split('.')[-1].lower()

            if file_extension == 'jpg':
                filename = image.save_image(request.files[file], file_extension)
                files_list.append(filename)

            if file_extension == 'gif':
                filename = image.save_image(request.files[file], file_extension)
                files_list.append(filename)

            if file_extension == 'png':
                filename = image.save_image(request.files[file], file_extension)
                files_list.append(filename)

        return {"mensagem": "Sua imagem foi enviada com sucesso!"}, 201

    except RequestEntityTooLarge:
        return {"mensagem":"Imagem maior que 1MB"}, 413

    except(Conflict):
        return {"mensagem":"Essa imagem já existe"}, 409

    except(UnsupportedMediaType):
        return {"mensagem":"Extensão de imagem não suportada"}, 415