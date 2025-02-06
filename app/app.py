import shutil
from flask import Flask, request, redirect, url_for, render_template, session, flash, send_from_directory
import sqlite3
import os

app = Flask(__name__)
# Gera uma chave secreta aleatória a cada execução
app.secret_key = os.urandom(24)

# Configurações
UPLOAD_FOLDER = '/var/www/html/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Conexão com o SQLite


def get_db_connection():
  conn = sqlite3.connect('auth.db')
  conn.row_factory = sqlite3.Row
  return conn

# Verifica se o usuário está autenticado


def is_authenticated():
  return 'username' in session


# Rota para excluir uma pasta e seus arquivos


@app.route('/delete_folder/<folder_name>', methods=['GET'])
def delete_folder(folder_name):
  if not is_authenticated():
    return redirect(url_for('login'))

  # Caminho completo para a pasta a ser deletada
  folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)

  # Verifica se a pasta existe
  if os.path.exists(folder_path) and os.path.isdir(folder_path):
    try:
      # Remove a pasta e todo o seu conteúdo
      shutil.rmtree(folder_path)
      flash(f'Pasta "{folder_name}" excluída com sucesso!')
    except Exception as e:
      flash(f'Erro ao excluir a pasta: {e}')
  else:
    flash('A pasta não foi encontrada.')

  # Redireciona de volta para a lista de arquivos
  return redirect(url_for('list_files'))


@app.route('/files/<path:filename>')
def serve_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Rota para listar arquivos e pastas
@app.route('/files')
def list_files():
  def list_directory(path):
    result = []
    for item in os.listdir(path):
      item_path = os.path.join(path, item)
      if os.path.isdir(item_path):
        result.append({
            'type': 'directory',
            'name': item,
            # Recursivamente lista os conteúdos
            'contents': list_directory(item_path)
        })
      else:
        result.append({
            'type': 'file',
            'name': item
        })
    return result

  # Lista os arquivos e pastas no diretório de upload
  files = list_directory(app.config['UPLOAD_FOLDER'])
  return render_template('files.html', files=files)


# Rota para a página de login


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
      session['username'] = username
      return redirect(url_for('upload'))
    else:
      flash('Usuário ou senha inválidos.')

  return render_template('login.html')

# Rota para a página inicial (após login)


@app.route('/')
def upload():
  if not is_authenticated():
    return redirect(url_for('login'))

  return render_template('upload.html')

# Rota para processar o upload


@app.route('/upload', methods=['POST'])
def upload_file():
  if not is_authenticated():
    return redirect(url_for('login'))

  if 'file' not in request.files:
    flash('Nenhum arquivo enviado.')
    return redirect(url_for('upload'))

  file = request.files['file']
  part_size = int(request.form['part_size'])  # Tamanho de cada parte em bytes

  if file.filename == '':
    flash('Nenhum arquivo selecionado.')
    return redirect(url_for('upload'))

  if file:
    # Cria a pasta com o nome do arquivo
    file_name = os.path.splitext(file.filename)[0]
    file_dir = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    os.makedirs(file_dir, exist_ok=True)

    # Salva o arquivo completo
    file_path = os.path.join(file_dir, file.filename)
    file.save(file_path)

    # Divide o arquivo em partes
    with open(file_path, 'rb') as f:
      part_number = 1
      while True:
        chunk = f.read(part_size)
        if not chunk:
          break
        part_file = os.path.join(file_dir, f"{file_name}_part{part_number}")
        with open(part_file, 'wb') as part:
          part.write(chunk)
        part_number += 1

    flash('Arquivo enviado e dividido com sucesso!')
    return redirect(url_for('upload'))

  flash('Erro ao processar o arquivo.')
  return redirect(url_for('upload'))


# Rota para logout


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('login'))


if __name__ == '__main__':
  # Cria o banco de dados SQLite se não existir
  conn = get_db_connection()
  conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
  conn.close()

  app.run(host='0.0.0.0', port=5000)
