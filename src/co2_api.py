import time
import os
import socket
import fcntl
import array
import struct
import importlib.metadata
import threading
from flask import Flask, jsonify
import RPi.GPIO as GPIO

try:
    APP_VERSION = importlib.metadata.version("co2-sensor")
except Exception:
    APP_VERSION = os.environ.get("APP_VERSION") or "undefined"

# 設定ファイル（settings.py）をインポート
try:
    import sys
    sys.path.insert(0, '/etc/co2-sensor')
    import settings
except ImportError:
    raise RuntimeError('settings.py が /etc/co2-sensor/ に見つかりません。')

app = Flask(__name__)
lock = threading.Lock()
LOCK_FILE = '/tmp/co2_sensor.lock'

PWM_PIN = getattr(settings, 'PWM_PIN', None)
if PWM_PIN is None:
    raise RuntimeError('PWM_PIN is not defined in settings.py')

def read_co2_pwm(timeout=5):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_PIN, GPIO.IN)
    start_time = time.time()

    try:
        # Wait for the first LOW signal
        while GPIO.input(PWM_PIN) == 1:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for LOW start")
        while GPIO.input(PWM_PIN) == 0:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for HIGH start")

        th_start = time.time()

        while GPIO.input(PWM_PIN) == 1:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for HIGH end")

        th_end = time.time()

        while GPIO.input(PWM_PIN) == 0:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for LOW end")

        tl_end = time.time()

        th = th_end - th_start
        tl = tl_end - th_end

        co2 = 5000 * th / (th + tl)
        return {'co2': round(co2, 1)}

    finally:
        GPIO.cleanup(PWM_PIN)


def get_all_ipv4_addresses():
    ip_list = []
    try:
        max_possible = 128  # 十分な数のインターフェースを想定
        bytes = max_possible * 32
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        names = array.array('B', b'\0' * bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(), 0x8912,
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        namestr = names.tobytes()
        for i in range(0, outbytes, 40):
            ip = namestr[i+20:i+24]
            ip_addr = socket.inet_ntoa(ip)
            if not ip_addr.startswith('127.') and ip_addr not in ip_list:
                ip_list.append(ip_addr)
    except Exception:
        pass
    return ip_list

@app.route('/co2', methods=['GET'])
def get_co2():
    hostname = socket.gethostname()
    ip_addresses = get_all_ipv4_addresses()
    retry = 0
    max_retry = 10
    co2_value = None
    error_detail = None
    while retry < max_retry:
        try:
            with open(LOCK_FILE, 'w') as lockfile:
                fcntl.flock(lockfile, fcntl.LOCK_EX)
                value = read_co2_pwm()
                fcntl.flock(lockfile, fcntl.LOCK_UN)
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
            'ip': ip_addresses,
            'version': APP_VERSION
        }), 200
    else:
        return jsonify({
            'result': 'error',
            'co2': None,
            'hostname': hostname,
            'ip': ip_addresses,
            'version': APP_VERSION,
            'error': error_detail
        }), 500
