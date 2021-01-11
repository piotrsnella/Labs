from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/strona')
def moja_strona():
    return """
    <h1>Moja pierwsza strona we Flask</h1>
    <p>Pierwszy paragraf zapisany w znaczniku <b>p</b>.</p>
    """

@app.route('/user/<int:id>')
def get_user_id(id):
    return {id: 'jan'}

@app.route('/sum/<int:a>/<int:b>')
def get_sum(a, b):
    return f'Suma liczb {a} oraz {b} wynosi: {a+b}'

# parametry url
@app.route('/sum_params')
def get_sum_params():
    val_1 = request.args.get("val1", None)
    val_2 = request.args.get("val2", None)
    return str(int(val_1) + int(val_2)) # uwaga!, musimy zwrócić obiekt typu str, nie int

    
#@app.route('/index')
#def index():
 #   username="Jan"
  #  return render_template('index.html', name=username)

lista = ['Jan', 'Maria', 'Adam']
@app.route('/list_users')
def list_users():
    return{'lista': lista}
    
    
@app.route('/list_users/<int:number_of_users>')
def list_users_slices_1(number_of_users):
    return {'lista': lista[:number_of_users]}

@app.route('/list_users_slice')
def list_users_slice_2():
    number_of_users = request.args.get('number_of_users', len(lista))
    return {'lista': lista[:number_of_users]}


from flask import render_template
@app.route('/index')
def index():
    zmienna = "Jan"
    return render_template('index.html', name=zmienna)

@app.route('/list_users_template')
def list_users_template():
    return render_template('list.html', lista_uzytkownikow=lista)
    
@app.route('/list_users_template_1/<int:number_of_users>')
def list_users_slice_template_1(number_of_users):
    return render_template('list.html', lista_uzytkownikow = lista[:number_of_users])

@app.route('/list_users_template_2')
def list_users_slice_template_2():
    val = request.args.get('number_of_users',len(lista))
    val = int(val)
    return render_template('list.html', lista_uzytkownikow = lista[:val])
    
# ładowanie plików na serwer
from flask import request
from werkzeug.utils import secure_filename
import os

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['plik']
        filename = secure_filename(f.filename)
        print('nazwa pliku', filename)
        name_with_dir = os.path.join('wrzucone_pliki', filename)
        f.save(name_with_dir)
        return f"plik <b>{filename}</b> został zapisany w lokalizacji '{name_with_dir}'."
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__=="__main__":
    app.run(debug=True, port=1234)
