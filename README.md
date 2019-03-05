# hihobot-tts
自分のように対話し、自分の声で音声合成するライブラリのWebAPI化する

## 使い方
### 機械学習モデルを準備
[hihobot](https://github.com/Hiroshiba/hihobot)と[hihobot-synthesis](https://github.com/Hiroshiba/hihobot-synthesis)

### 必要なライブラリの準備
```bash
pipenv install
```

## 実行
```bash
pipenv run python run.py --config_path sample_config.json --port 8000
```

## ライセンス
MIT License
