# ステップアップ

ここから先は「余力がある人向け」の課題です。当日やってもいいし、宿題にしてもOKです。

## チャレンジ課題

1. `02_chat_stream.py` の `messages` を書き換えて、AIに「伊予弁で話すエンジニア」という役割を与えてみよう
2. `ollama pull` で他のモデル（`phi3`, `llama3` など）を試して、回答の精度や速さを比較してみよう
3. AIの回答をJSON形式で返させて、Pythonの辞書として扱ってみよう
4. `03_vision.py` で画像認識を試してみよう（下記参照）

## 画像認識（Vision）を試す

`ollama show モデル名` で **Capabilities** に `vision` があるモデルは画像認識に対応しています。

```bash
# モデルの対応機能を確認
ollama show gemma3:4b
# → Capabilities に "vision" と表示されればOK

# 画像を渡して説明させる
python 03_vision.py photo.jpg

# プロンプトを変えることもできます
python 03_vision.py photo.jpg --prompt "この画像に写っている文字を読み取ってください"
```

> **注意:** `gemma3:1b` は vision 非対応です。画像認識を試すには `gemma3:4b` 以上を使ってください。

## 愛媛弁キャラの Modelfile

Ollama では `Modelfile` を使って独自のキャラクターを定義できます（Docker の Dockerfile に似た仕組みです）。
`FROM` でベースにするモデルを指定し、`SYSTEM` でそのモデルのシステムプロンプト（役割・口調など）を固定できます。

```Modelfile
FROM gemma3:1b
SYSTEM あなたは愛媛在住のベテランエンジニアです。親しみやすい伊予弁で、初心者にもわかりやすく技術を教えてください。
```

```bash
# カスタムモデルの作成
ollama create ehime-engineer -f Modelfile

# 実行
ollama run ehime-engineer
```

`PARAMETER` での推論設定など、他の命令や詳しい構文は公式リファレンスを参照してください。

https://docs.ollama.com/modelfile

より詳しい解説はこちらの記事もどうぞ。

https://zenn.dev/kazweda/articles/093dd95dc509c0

## ローカル RAG（応用）

インターネットを使わずに、手元の PDF やドキュメントを AI に読み込ませる仕組みです。
`PyMuPDF` で PDF を読み込み、Ollama の embeddings モデルで検索エンジンを作ります。

より詳しい解説はこちらの記事もどうぞ。

https://zenn.dev/kazweda/articles/57a9e1d8a32154
