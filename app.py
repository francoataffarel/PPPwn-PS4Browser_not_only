# -*- coding: utf-8 -*-
# app.py

from flask import Flask, request, render_template_string, jsonify
import subprocess

app = Flask(__name__)

# HTML template para a interface com o botão
HTML = """
<html>
<head>
<title>PPPwn-Flask Jailbreak</title>
</head>
<body>
    <h1>PPPwn Jailbreak Interface</h1>
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

@app.route('/start_exploit', methods=['POST'])
def start_exploit():
    # Configuração padrão para executar o pppwn
    command = [
        "/usr/local/bin/pppwn",
        "--interface", "en0",
        "--fw", "1100",
        "--stage1", "/data/stage1.bin",
        "--stage2", "/data/stage2.bin",
        "--auto-retry"
    ]
    try:
        # Executa o comando pppwn
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return jsonify({'status': 'success', 'output': result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

