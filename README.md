# Ollama + Python ハンズオン

PyEhime 勉強会用のハンズオン教材です。
ローカルLLM（Ollama）を Python から操作し、軽量なモデルを手元のPCだけで（オフラインでも）動かす体験をします。

```
ollama-handson/
├── README.md           # 手順書（メイン）
├── STEP_UP.md          # 余力がある人向けのステップアップ課題
├── requirements.txt    # 必要なライブラリ (ollama など)
├── .gitignore          # Python用の設定
├── 01_check_ollama.py  # 疎通確認用（一番シンプルなコード）
├── 02_chat_stream.py   # チャット形式（ストリーミング）：TODOを埋めて完成させます
└── 03_vision.py        # 画像認識（vision）：TODOを埋めて完成させます
```

---

## なぜローカルLLM？

ChatGPT などのクラウドAIと違い、Ollama のローカルモデルは**モデルのダウンロードさえ済めば、インターネットに接続しなくても動きます**。

- **データが外に出ない**: プロンプトや回答は手元のPCの中だけで処理されます。社内文書・顧客情報・ソースコードなど、外部サービスに送れない情報も扱えます
- **ネットワークを遮断した環境で使える**: 社内の閉じたネットワーク、Webアクセスが制限された端末、電波の届かない現場や移動中でも動きます
- **利用料やアクセス制限を気にせず試せる**: API の従量課金や回数制限がなく、何度でも試行錯誤できます
- **同じモデルを使い続けられる**: ダウンロードしたモデルは手元に残るので、提供元の仕様変更や提供終了の影響を受けにくくなります

一方で、軽量モデルは大規模なクラウドAIに比べると精度や知識量で劣ります。「どんな用途なら軽量モデルで十分か」を体感するのも、このハンズオンの目的のひとつです。

> **試してみよう:** 事前準備の動作確認ができたら、Wi-Fi を切った状態でもう一度 `01_check_ollama.py` や `02_chat_stream.py` を動かしてみてください。オフラインでも返事が返ってくるはずです。

> **注意:** Ollama には `gemma4:cloud` のように `:cloud` が付いたクラウドモデルや Web 検索の機能もあり、これらを使うとプロンプトは Ollama のサーバーに送られます。ローカルモデルだけを使いたい場合は、環境変数 `OLLAMA_NO_CLOUD=1` を設定するか、`~/.ollama/server.json` に `{"disable_ollama_cloud": true}` と書いてから Ollama を再起動すると、クラウド機能を無効にできます（[公式FAQ](https://docs.ollama.com/faq)）。

---

## 事前準備

Git・Python・VS Code のインストール手順（Windows/Mac別）は事前準備ガイド記事にまとめてあります。まだお済みでない方は先にご覧ください。

👉 [ハンズオン事前準備ガイド](https://netplan.co.jp/blog/2026/2026-08-14-handson-preparation-guide/)

準備ができたら、このリポジトリをクローンしてください（`~/repos` など、クラウド同期対象外のフォルダがおすすめです）。

```bash
mkdir -p ~/repos && cd ~/repos
git clone https://github.com/kazweda/ollama-handson.git
cd ollama-handson
```

### 1. Ollama のインストール

https://ollama.com/download からダウンロードしてインストールしてください。

Ollama はデスクトップアプリとしても動作し、モデルのダウンロード・切り替えや、
チャットUIでの対話、画像・PDFのドラッグ&ドロップなど、GUIだけでも色々なことができます。
このハンズオンでは「モデルを起動しておき、裏側で動くAPIサーバーとしてPythonから呼び出す」
使い方がメインですが、興味がある方はアプリ単体でも触ってみてください。
詳しくは公式ドキュメント（https://docs.ollama.com/ ）を参照してください。

### 2. Python 環境

Python 3.11 以上を推奨します（3.10 は2026年10月でサポート終了のため）。お使いのPCにそれより新しいバージョンが入っていれば、そちらでも問題ありません。

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

モデルのダウンロードには時間がかかるため、先に済ませておきましょう（勉強会で参加する場合は、会場のネットワーク混雑を避けるため**事前に**お願いします）。

| モデル | サイズ | 特徴 |
|---|---|---|
| `gemma3:1b` | 約1GB | 軽量で高速。低スペックPCでも安心 |
| `gemma3:4b` | 約3GB | より自然な日本語。メモリに余裕があればおすすめ |

どちらか1つでOKです。迷ったら `gemma3:1b` から始めましょう。

> より新しい Gemma4 も公開されています。軽量化された QAT 版（`gemma4:e2b-it-qat` など）なら最小約4.3GBまで抑えられますが、それでも `gemma3:4b`（約3GB）より重く、低スペックPCでの体験を優先するため本ハンズオンでは Gemma3 を採用しています。

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

## はじめに（Intro）

### 最初のステップ

1. Ollama をインストールする
2. Python から Ollama を呼び出して、返事が返ってくることを確認する
3. ストリーミング形式でチャットしてみる

これだけできれば、このハンズオンの目標は達成です。

> `02_chat_stream.py` と `03_vision.py` は `# TODO` の部分を埋めて完成させる形式になっています。
> 詰まったときは `solution` ブランチに完成版があるので、参考にしてください。

### 構造化出力（Structured Output）

慣れてきたら、AIの回答をJSON形式で受け取ることに挑戦してみましょう。
プログラムの一部として LLM を組み込むときに必須のテクニックです。

例：ニュース記事を渡して `{"title": "...", "summary": "...", "keywords": [...]}` 形式で返させる

---

## Tips

### VS Code を使っている方へ

セットアップ方法や `import ollama` の波線（警告）対処は[事前準備ガイド](https://netplan.co.jp/blog/2026/2026-08-14-handson-preparation-guide/)を参照してください。

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

