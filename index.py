from flask import Flask, render_template, request, send_from_directory, redirect
from werkzeug.utils import secure_filename
import os
import moviepy.editor as mp

app = Flask(__name__)

UPLOAD_FOLDER = 'videos'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    f = request.files['arquivo']
    if f.filename:
      nomeArquivo = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeArquivo))

      #Converter
      path = os.path.join(app.config['UPLOAD_FOLDER'], nomeArquivo)
      nome = f.filename.split('.')[0]

      clip = mp.VideoFileClip(path).subclip()
      clip.audio.write_audiofile(f'audio/{nome}.mp3')

      arquivo = "video.mp3"

      return render_template('index.html', TudoOK=True, arquivoBaixar=arquivo)
    else:
      return render_template('index.html', deuErro=True)
    
@app.route('/download/<arquivo>')
def download(arquivo):
  return send_from_directory('audio', arquivo, as_attachment=True)

