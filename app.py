# -*- coding: utf-8 -*-
# app.py

from flask import Flask, request, jsonify
from celery import Celery

# Supondo que todos os outros módulos e classes necessárias foram importadas
from  PPPwn.pppwn_exploit import *

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

DEFAULT_INTERFACE = "enp1s0"

def run_exploit(interface, firmware='1100', stage1='PPPwn/PS4_stage_bin_all/PS4-11.00/stage1/stage1.bin', stage2='PPPwn/PS4_stage_bin_all/PS4-11.00/stage2/stage2.bin'):
    # Leitura dos arquivos binários
    with open(stage1, mode='rb') as f:
        stage1_data = f.read()

    with open(stage2, mode='rb') as f:
        stage2_data = f.read()

    # Determinação da versão do firmware
    firmware_mapping = {
        '750': OffsetsFirmware_750_755(),
        '751': OffsetsFirmware_750_755(),
        '755': OffsetsFirmware_750_755(),
        '800': OffsetsFirmware_800_803(),
        '801': OffsetsFirmware_800_803(),
        '803': OffsetsFirmware_800_803(),
        # Inclua os demais conforme necessário
        '1100': OffsetsFirmware_1100(),
    }
    offs = firmware_mapping.get(firmware, OffsetsFirmware_1100())

    exploit = Exploit(offs, interface, stage1_data, stage2_data)
    result = exploit.run()
    return result

@celery.task
def perform_exploit(interface, firmware):
    return run_exploit(interface, firmware)

@app.route('/start_exploit', methods=['POST'])
def start_exploit():
    data = request.get_json(silent=True)  # Usa get_json com silent=True para retornar None se não houver dados
    if data is None:
        data = {}  # Define data como um dicionário vazio se não houver corpo na requisição
    interface = data.get('interface', DEFAULT_INTERFACE)  # Valor padrão é `wlp2s0`
    firmware = data.get('firmware', '1100')  # Firmware padrão é `1100`
    task = perform_exploit.apply_async((interface, firmware))
    return jsonify({'task_id': task.id}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000,debug=True)
