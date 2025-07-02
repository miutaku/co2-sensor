# co2-sensor

Raspberry Pi用MH-Z19 CO2センサーAPIサーバ

## 概要

このアプリケーションは、Raspberry Pi上でMH-Z19 CO2センサーから値を取得し、APIリクエストでJSON形式で返します。

- Python 3.13対応
- mh_z19ライブラリ利用
- FlaskによるAPIサーバ（localhost:8080）
- systemdサービス化対応
- deb/rpmパッケージ化対応
- GitHub Actionsでビルド＆リリース

## インストール

### 依存パッケージ

```
sudo apt update
sudo apt install python3 python3-pip python3-flask python3-setuptools
sudo pip3 install mh-z19
```

### パッケージからインストール（推奨）

#### debパッケージ（Debian/Ubuntu/Raspberry Pi OS）
```
sudo dpkg -i co2-sensor_*.deb
```

#### rpmパッケージ（Fedora/RHEL系）
```
sudo dnf install ./co2-sensor-*.rpm
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
  "co2": 605.0
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
