import mh_z19
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/co2', methods=['GET'])
def get_co2():
    try:
        value = mh_z19.read_from_pwm()
        if value and 'co2' in value:
            return jsonify({'co2': value['co2']}), 200
        else:
            return jsonify({'error': 'CO2 value not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
