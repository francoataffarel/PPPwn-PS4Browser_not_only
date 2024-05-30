# -*- coding: utf-8 -*-
# app.py

from flask import Flask, request, render_template_string, jsonify
from celery import Celery
import subprocess

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# HTML template para a interface com o botão
HTML = """
<html>
<head>
<title>PPPwn-PS4Browser_not_only</title>
</head>
<body>
    <h1>PPPwn Jailbreak via WWW-App PS4</h1>
    <form action="/start_exploit" method="post">
        <button type="submit">JAILBREAK!</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    # Retorna a página HTML com o botão
    return render_template_string(HTML)

@celery.task(bind=True)
def run_pppwn(self):
    # Configuração padrão para executar o pppwn
    command = [
        "/usr/local/bin/pppwn",
        "--interface", "enp1s0",
        "--fw", "1100",
        "--stage1", "/app/data/1100/stage1.bin",
        "--stage2", "/app/data/1100/stage2.bin",
        "--auto-retry"
    ]
    try:
        # Executa o comando pppwn
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return {'status': 'success', 'output': result.stdout}
    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'output': e.stderr}

@app.route('/start_exploit', methods=['POST'])
def start_exploit():
    # Chama a tarefa run_pppwn de forma assíncrona
    task = run_pppwn.apply_async()
    return jsonify({'task_id': task.id}), 202

@app.route('/status/<task_id>')
def task_status(task_id):
    task = run_pppwn.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
            'result': task.info
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

