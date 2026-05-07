```
ollama-handson/
├── README.md           # 当日の手順書（メイン）
├── requirements.txt    # 必要なライブラリ (ollama など)
├── .gitignore          # Python用の設定
├── 01_check_ollama.py  # 疎通確認用（一番シンプルなコード）
└── 02_chat_stream.py   # チャット形式（ストリーミング）のサンプル
```
## 事前準備

### Ollama install URL
https://ollama.com/download

### Python環境
Python環境（3.10以上推奨）
```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
# Windowsの場合:
.venv\Scripts\activate
# Mac/Linuxの場合:
source .venv/bin/activate

# ライブラリのインストール
pip install -r requirements.txt
```

### モデルのダウンロード
当日のネットワーク混雑を避けるため、事前に ollama pull gemma2:2b をしておいてください
```bash
ollama pull gemma2:2b
```

### サンプルコードの実行
```bash
python 01_check_ollama.py
```
