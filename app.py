
# -*- coding: utf-8 -*-
# app.py

from flask import Flask, render_template_string, redirect, url_for, Response, stream_with_context
import subprocess
import threading
import logging
import time
import psutil
import os
import atexit

app = Flask(__name__)

# Configurando o logger
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# HTML template para a interface com o botão
HTML = """
<!DOCTYPE html>
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

lock_file = "/tmp/pppwn.lock"

def remove_lock_file():
    if os.path.exists(lock_file):
        os.remove(lock_file)
        logging.info("Lock file removed on exit.")

atexit.register(remove_lock_file)

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/start_exploit', methods=['POST'])
def start_exploit():
    if is_process_running("/usr/local/bin/pppwn"):
        return "PPPwn is already running. Please wait for it to complete.", 409
    threading.Thread(target=run_pppwn).start()
    return redirect(url_for('output'))

def is_process_running(process_path):
    for proc in psutil.process_iter(['exe']):
        if proc.info['exe'] == process_path:
            return True
    return False

def run_pppwn():
    if os.path.exists(lock_file):
        logging.info("PPPwn is already running.")
        return
    try:
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        command = [
            "/usr/local/bin/pppwn",
            "--interface", "enp1s0",
            "--fw", "1100",
            "--stage1", "/app/data/1100/stage1.bin",
            "--stage2", "/app/data/1100/stage2.bin",
            "--auto-retry"
        ]
        logging.info(f"Starting command: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open('app.log', 'a') as f:
            for line in iter(process.stdout.readline, ''):
                logging.info(line.strip())
                f.write(line)
                f.flush()
        process.wait()
        logging.info("PPPwn process finished.")
    except Exception as e:
        logging.error(f"An error occurred while running PPPwn: {e}")
    finally:
        remove_lock_file()

@app.route('/output')
def output():
    def generate():
        log_file = "app.log"
        with open(log_file) as f:
            while True:
                where = f.tell()
                line = f.readline()
                if not line:
                    time.sleep(1)
                    f.seek(where)
                else:
                    yield line.strip() + "\n"
    return Response(stream_with_context(generate()), mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)