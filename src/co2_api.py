import mh_z19
from flask import Flask, jsonify
import socket
import time
import os
import argparse
import importlib.metadata

try:
    APP_VERSION = importlib.metadata.version("co2-sensor")
except Exception:
    APP_VERSION = os.environ.get("APP_VERSION") or "undefined"

app = Flask(__name__)

@app.route('/co2', methods=['GET'])
def get_co2():
    hostname = socket.gethostname()
    retry = 0
    max_retry = 10
    co2_value = None
    error_detail = None
    while retry < max_retry:
        try:
            value = mh_z19.read_from_pwm()
            if value and 'co2' in value:
                co2_value = value['co2']
                break
            else:
                error_detail = 'CO2 value not found'
        except Exception as e:
            if "GPIO busy" in str(e):
                time.sleep(1)
                retry += 1
                error_detail = str(e)
                continue
            else:
                error_detail = str(e)
                break
    if co2_value is not None:
        return jsonify({
            'result': 'ok',
            'co2': co2_value,
            'hostname': hostname,
            'version': APP_VERSION
        }), 200
    else:
        return jsonify({
            'result': 'error',
            'co2': None,
            'hostname': hostname,
            'version': APP_VERSION,
            'error': {
                'detail': error_detail
            }
        }), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CO2 Sensor API')
    parser.add_argument('--version', action='store_true', help='Show version and exit')
    args = parser.parse_args()
    if args.version:
        print(APP_VERSION)
    else:
        app.run(host='0.0.0.0', port=8080)
