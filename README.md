# Ollama + Python ハンズオン

PyEhime 勉強会用のハンズオン教材です。
ローカルLLM（Ollama）を Python から操作する体験をします。

```
ollama-handson/
├── README.md           # 当日の手順書（メイン）
├── STEP_UP.md          # 余力がある人向けのステップアップ課題
├── requirements.txt    # 必要なライブラリ (ollama など)
├── .gitignore          # Python用の設定
├── 01_check_ollama.py  # 疎通確認用（一番シンプルなコード）
├── 02_chat_stream.py   # チャット形式（ストリーミング）のサンプル
└── 03_vision.py        # 画像認識（vision）のサンプル
```

---

## はじめに（Intro）

### 最初のステップ

1. Ollama をインストールする
2. Python から Ollama を呼び出して、返事が返ってくることを確認する
3. ストリーミング形式でチャットしてみる

これだけできれば、今日の目標は達成です。

### 構造化出力（Structured Output）

慣れてきたら、AIの回答をJSON形式で受け取ることに挑戦してみましょう。
プログラムの一部として LLM を組み込むときに必須のテクニックです。

例：ニュース記事を渡して `{"title": "...", "summary": "...", "keywords": [...]}` 形式で返させる

---

## 事前準備

### 1. Ollama のインストール

https://ollama.com/download からダウンロードしてインストールしてください。

Ollama はデスクトップアプリとしても動作し、モデルのダウンロード・切り替えや、
チャットUIでの対話、画像・PDFのドラッグ&ドロップなど、GUIだけでも色々なことができます。
今日のハンズオンでは「モデルを起動しておき、裏側で動くAPIサーバーとしてPythonから呼び出す」
使い方がメインですが、興味がある方はアプリ単体でも触ってみてください。
詳しくは公式ドキュメント（https://docs.ollama.com/ ）を参照してください。

### 2. Python 環境

Python 3.11 以上を推奨します（3.10 は2026年10月にサポート終了予定のため）。お使いのPCにそれより新しいバージョンが入っていれば、そちらでも問題ありません。

インストールされていない場合は https://www.python.org/downloads/ からダウンロードしてください。

> 環境によっては `python` を `python3` に、`pip` を `pip3` に読み替えてください。

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

### 3. モデルのダウンロード

当日のネットワーク混雑を避けるため、**事前に**ダウンロードしておいてください。

| モデル | サイズ | 特徴 |
|---|---|---|
| `gemma3:1b` | 約1GB | 軽量で高速。低スペックPCでも安心 |
| `gemma3:4b` | 約3GB | より自然な日本語。メモリに余裕があればおすすめ |

どちらか1つでOKです。迷ったら `gemma3:1b` から始めましょう。

> より新しい Gemma4 も公開されていますが、最小サイズでも7GB前後と重く、低スペックPCでの体験を優先するため本ハンズオンでは Gemma3 を採用しています。

```bash
# 軽量版（おすすめ）
ollama pull gemma3:1b

# 高品質版（メモリに余裕がある方）
ollama pull gemma3:4b
```

> **動作環境の目安:** GPUがない一般的なノートPCでもCPUだけで動作します。目安として `gemma3:1b` はRAM 4GB程度〜、`gemma3:4b` はRAM 8GB程度〜あれば快適に動きます。お使いのPCのメモリが少ない場合は `gemma3:1b` を選んでください。

### 4. 動作確認

```bash
python 01_check_ollama.py
```

「接続成功です」のような返答が表示されれば準備完了です。

---

## Tips

### VS Code を使っている方へ

- 「Create a virtual environment?」という通知が出たら、**Yes** を選択すると環境構築がスムーズです。
- `import ollama` に波線（警告）が出る場合は、画面右下の Python バージョン表示をクリックし、`.venv` のインタープリタを選択してください。
- それでも消えない場合は `Cmd+Shift+P`（Windows: `Ctrl+Shift+P`）→「Python: Restart Language Server」を実行してください。

### よくあるエラー

| エラー | 原因 | 対処 |
|---|---|---|
| `could not connect to a running Ollama instance` | Ollama アプリが起動していない | Ollama アプリを起動する（メニューバー/タスクバーにアイコンが出ればOK） |
| `ConnectionError` | 同上 | 同上 |
| `model not found` / `NotFoundError` | モデル未ダウンロード | `ollama pull gemma3:1b` を実行 |
| `pip install` で「引数がない」エラー | ライブラリ名の指定忘れ | `pip install -r requirements.txt` または `pip install ollama` |
| `Import "ollama" could not be resolved` | VS Code が仮想環境を認識していない | 上記「VS Code を使っている方へ」を参照 |

---

## ステップアップ

余力がある人向けの課題（画像認識、Modelfile によるキャラ作成、ローカルRAGなど）は
[STEP_UP.md](STEP_UP.md) にまとめました。

---

動いたコードや面白いプロンプトがあれば、ぜひプルリクエストや Issue で教えてください!

