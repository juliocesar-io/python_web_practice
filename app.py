import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from collections import Counter

# Path donde se guardaran los archivos subidos
UPLOAD_FOLDER = '/Users/JulioC/PycharmProjects/flask-practice/media'
ALLOWED_EXTENSIONS = set(['txt'])


# Configuracion de la app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_words_dict(path):

    w_dic = {}
    with open(path) as f:
        words = [word.upper() for line in f for word in line.split()]
        c = Counter(words)
        for word, count in c.items():
            w_dic[word] = count

    return w_dic


def sort_words_dict(word_dict):

    words_tuple = tuple(word_dict.iteritems())
    words_sorted = sorted(sorted(words_tuple, key=lambda x: x[0])[:10], key=lambda x: x[1], reverse=True)

    return words_sorted


def word_search(key, word_dict):

    if key in word_dict:
        res = word_dict[key]
    else:
        res = {}

    return res


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Verificar que este en el formato permitido
        if file and allowed_file(file.filename):
            # Limpiar el nombre del archivo

            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Guardar archivo en el directorio definido
            file.save(path)

            # Obtener las palabras con su cuenta respectiva en un dicionario llave-valor

            words = get_words_dict(path)

            # Organizar por ocurrencia y orden alfabetico
            words_result_sorted = sort_words_dict(words)

            # Buscar una palabra dada
            search_key = request.form['buscar-palabra'].upper()

            search_result = word_search(search_key, words)

            return render_template('response.html', words_result=words_result_sorted, search_key=search_key,
                                   search_result=search_result)
    return render_template('form.html')


if __name__ == '__main__':
    app.secret_key = 'dasdx45345'
    app.run(debug=True, port=4545)
