from flask import Flask, request, jsonify, send_file
import os 
from werkzeug.exceptions import RequestEntityTooLarge, NotFound
from werkzeug.utils import send_from_directory
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
    
    try:
        for file in request.files:
            file_extension = request.files[file].filename.split('.')[-1].lower()
            filename = request.files[file].filename
            file_list = os.listdir(f'{files_directory}/{file_extension}')              

            if filename in file_list:
                return {"mensagem":"Essa imagem já existe"}, 409
            
            if file_extension == 'jpg':
                filename = image.save_image(request.files[file], file_extension)

            if file_extension == 'gif':
                filename = image.save_image(request.files[file], file_extension)

            if file_extension == 'png':
                filename = image.save_image(request.files[file], file_extension)

        return {"mensagem": "Sua imagem foi enviada com sucesso!"}, 201

    except RequestEntityTooLarge:
        return {"mensagem":"Imagem maior que 1MB"}, 413
    
    except FileNotFoundError:
                return {"mensagem":"Extensão de imagem não suportada"}, 415

@app.get("/files")
def get_files(): 
    image_list = image.get_files()
    return image_list, 200

@app.get('/files/<formato>')
def get_list_specific_format(formato):

    try:
        if formato == 'jpg':
            image_jpg_list = image.list_by_extension('jpg')
            return jsonify(image_jpg_list), 200
        if formato == 'png':
            image_png_list = image.list_by_extension('png')
            return jsonify(image_png_list), 200
        if formato == 'gif':
            image_gif_list = image.list_by_extension('gif')
            return jsonify(image_gif_list), 200
        
        else:
            raise NotFound
    except NotFound:
        return {"mensagem": "Formato inválido"}, 404


@app.get('/download/<filename>')
def download_image_by_name(filename):

    try:
        extension = filename.split('.')[-1]
        if extension == 'jpg' or extension == 'png' or extension == 'gif':
            path = image.get_path(filename, extension)
            return send_file(path, as_attachment=True), 200
        else:
            raise FileNotFoundError
 
    except FileNotFoundError:
        return {"mensagem": "Arquivo não encontrado"}, 404


# @app.get('/download-zip')
# def download_zip():
#     query_params = request.args.get("file_extension")
#     directory=f'{files_directory}/{query_params}'
#     try:
#         if os.listdir(directory) == []:
#             return jsonify(message = "There are no files in the requestor directory"), 409    
#         else:
#             image.zip_image(query_params, directory)
#             return jsonify(message = "Success"), 200   
#     except:
#         return jsonify(message="File does not exist"), 404

# @app.get('/download-zip')
# def download_zip():
#     query_params = request.args.get("extension")
#     directory = f'{files_directory}/{query_params}'
#     try:
#         if os.listdir(directory) == []:
#             return jsonify("não há arquivos")
#         else:
#             files_list = image.zip_file(os.listdir(directory))
#             return image.save_image(files_list, query_params), 200
#     except:
#         return 'erro', 400


@app.get('/download-zip')
def downloadZip():
    file_extension = request.args.get('file_extension')
    compression_rate = request.args.get('compression_rate')

    if (int(compression_rate) < 6 or int(compression_rate) == False):
        compression_rate = 6

    os.system(f'zip -r zip/{file_extension}.zip {files_directory}/{file_extension} * -{compression_rate}')

    return send_from_directory(
        directory="./zip", 
        path=f'{file_extension}.zip', 
        as_attachment=True
    ), 200