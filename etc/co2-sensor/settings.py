# gunicorn/Flask用 設定ファイル例

# CO2センサーPWM信号を接続したRaspberry PiのGPIO番号（BCM番号）
PWM_PIN = 12

# Flaskアプリの設定例
BIND = '0.0.0.0:8080'
WORKERS = 2
