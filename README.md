# co2-sensor

Raspberry Pi用MH-Z19 CO2センサーAPIサーバ

## 概要

このアプリケーションは、Raspberry Pi上でMH-Z19 CO2センサーから値を取得し、APIリクエストでJSON形式で返します。

- FlaskによるAPIサーバ（localhost:8080）
- systemdサービス化対応
- deb/rpmパッケージ化対応

## 設定ファイル

パッケージインストール時、設定ファイルは `/etc/co2-sensor/settings.py` に配置されます。

```
# settings.py の例
PWM_PIN = 12  # CO2センサーPWM信号を接続したRaspberry PiのGPIO番号（BCM番号）
BIND = '0.0.0.0:8080'  # gunicorn用バインドアドレス
WORKERS = 2            # gunicorn用ワーカ数
```

- `PWM_PIN` は必須です。未設定の場合は起動時にエラーとなります。
- 必要に応じて `/etc/co2-sensor/settings.py` を編集してください。

## インストール

### パッケージからインストール（推奨）

#### debパッケージ（Debian/Ubuntu/Raspberry Pi OS）
```
sudo dpkg -i co2-sensor_*.deb
```

#### rpmパッケージ（Fedora/RHEL系）
```
sudo dnf install ./co2-sensor-*.rpm
```

- 依存パッケージや systemd サービス登録も自動で行われます。
- サービスは `co2-sensor` という名前で登録されます。

### 依存パッケージ（手動インストールの場合のみ）

```
sudo apt update
sudo apt install python3 python3-pip python3-flask python3-setuptools
sudo pip3 install -r requirements.txt
```

## サービス起動

```
sudo systemctl enable co2-sensor
sudo systemctl start co2-sensor
```

## API 仕様

- エンドポイント: `GET /co2`
- レスポンス例:

```
{
  "result": "ok",
  "co2": 605.0,
  "hostname": "raspberrypi",
  "ip": ["192.168.1.10"],
  "version": "1.2.3"
}
```

## 開発・ビルド

### 手動実行

```
python3 src/co2_api.py
```

### パッケージビルド

```
python3 setup.py sdist
```

## GitHub Actionsによるリリース

`.github/workflows/release.yml` を参照してください。

## ライセンス

MIT
