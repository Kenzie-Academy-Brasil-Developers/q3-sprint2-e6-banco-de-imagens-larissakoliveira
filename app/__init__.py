from flask import Flask, request, jsonify, send_file
import os 
from werkzeug.exceptions import RequestEntityTooLarge, NotFound
from .kenzie import image

app = Flask(__name__)   

files_directory = os.getenv('FILES_DIRECTORY')
max_content_length = int(os.getenv('MAX_CONTENT_LENGTH'))
allowed_extensions = os.getenv('ALLOWED_EXTENSIONS').split(',')

app.config['MAX_CONTENT_LENGTH'] = int(max_content_length)

if not os.path.isdir(files_directory):
    os.mkdir(files_directory)
    for extension in allowed_extensions:
        path = f"{files_directory}/{extension}"
        os.makedirs(path)
            
@app.post("/upload")
def post_file(): 
    files_list = []
   

    try:
        for file in request.files:
            
            file_extension = request.files[file].filename.split('.')[-1].lower()
            filename = request.files[file].filename
            file_list = os.listdir(f'{files_directory}/{file_extension}')              
            

            if file_extension != 'png' and file_extension != 'jpg' and file_extension != 'gif':
                return {"mensagem":"Extensão de imagem não suportada"}, 415

            if filename in file_list:
                return {"mensagem":"Essa imagem já existe"}, 409
            
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
    
    except FileNotFoundError:
                return {"mensagem":"Extensão de imagem não suportada"}, 415

    # except Conflict:
    #     return {"mensagem":"Essa imagem já existe"}, 409

    # except UnsupportedMediaType:
    #     return {"mensagem":"Extensão de imagem não suportada"}, 415

@app.get("/files")
def get_files(): 
    image_list = image.list_all('all')
    return jsonify(image_list), 200

# @app.get('/files/jpg')
# def get_jpg(): 
#     try:
#         image_jpg_list = image.list_all('jpg')
#         return jsonify(image_jpg_list), 200
#     except NotFound:
#         return {"mensagem":"extensão inválida"}, 404
    
# @app.get('/files/png')
# def get_png(): 
#     image_png_list = image.list_all('png')
#     return jsonify(image_png_list), 200

# @app.get('/files/gif')
# def get_gif(): 
#     image_gif_list = image.list_all('gif')
#     return jsonify(image_gif_list), 200


@app.get('/files/<formato>')
def get_list_specific_format(formato):

    try:
        if formato == 'jpg':
            image_jpg_list = image.list_all('jpg')
            return jsonify(image_jpg_list), 200
        if formato == 'png':
            image_png_list = image.list_all('png')
            return jsonify(image_png_list), 200
        if formato == 'gif':
            image_gif_list = image.list_all('gif')
            return jsonify(image_gif_list), 200
    except NotFound:
        return {"mensagem": "Formato inválido"}, 404


@app.get('/download/<filename>')
def download_image_by_name(filename):

    try:
        extension = filename.split('.')[-1]
        if extension == 'jpg' or extension == 'png' or extension == 'gif':
            path = image.get_path(filename, extension)
            return send_file(path, as_attachment=True), 200
    except TypeError:
        return {"mensagem": "Nome de arquivo inválido"}, 404

#?<query_params>
@app.get("/download-zip")
def zip_download():

    if request.args.get("extension"):
        path = image.zip_images()