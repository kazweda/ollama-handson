# ステップアップ

ここから先は「余力がある人向け」の課題です。基本の手順が終わったら、興味のあるものから試してみてください。

## チャレンジ課題

1. `02_chat_stream.py` の `messages` を書き換えて、AIに「伊予弁で話すエンジニア」という役割を与えてみよう
2. `ollama pull` で他のモデル（`phi3`, `llama3`, `qwen3.5:4b` など）を試して、回答の精度や速さを比較してみよう
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

> **他の選択肢:** `qwen3.5` シリーズは軽量サイズながら標準でテキスト・画像の両方に対応しています。テキストと画像認識を1つのモデルで使い分けたい場合はこちらを試してみてください。
>
> - `qwen3.5:0.8b`（約1GB）: `gemma3:1b` と同程度の軽さで vision にも対応
> - `qwen3.5:2b`（約2.7GB）: `gemma3:4b` よりやや軽量な中間サイズ
> - `qwen3.5:4b`（約3.4GB）: 精度重視ならこちら
>
> ```bash
> ollama pull qwen3.5:0.8b
> ```

## 愛媛弁キャラの Modelfile

Ollama では `Modelfile` を使って独自のキャラクターを定義できます（Docker の Dockerfile に似た仕組みです）。
`FROM` でベースにするモデルを指定し、`SYSTEM` でそのモデルのシステムプロンプト（役割・口調など）を固定できます。

```Modelfile
FROM gemma3:1b
SYSTEM """
あなたは愛媛在住のベテランエンジニアです。親しみやすい伊予弁で、初心者にもわかりやすく技術を教えてください。
"""
PARAMETER temperature 0.7
```

- `SYSTEM` は `"""` で囲むと複数行で書けます
- `PARAMETER temperature` は応答のランダムさです。低いほど安定した答えに、高いほど多様な答えになります

```bash
# カスタムモデルの作成
ollama create ehime-engineer -f Modelfile

# 実行
ollama run ehime-engineer
```

> 上の内容を保存した `Modelfile` は `solution` ブランチにあります。

他の `PARAMETER` や命令、詳しい構文は公式リファレンスを参照してください。

https://docs.ollama.com/modelfile

より詳しい解説はこちらの記事もどうぞ。

https://zenn.dev/kazweda/articles/093dd95dc509c0

## 語学学習パートナーにしてみよう

チャレンジ課題1（伊予弁エンジニア）と同じ要領で、`02_chat_stream.py` の `messages` に `system` ロールを追加するだけで、英会話・スペイン語会話の練習相手にすることもできます。会話ループ自体はそのまま使えます。

```python
messages=[
    {'role': 'system', 'content': system_prompt},
    {'role': 'user', 'content': user_input},
]
```

### 英会話パートナー

```
あなたはフレンドリーな英会話パートナーです。会話は基本的に英語で行い、ユーザーの発言にスペルミスや
多少崩れた表現があっても意図を汲み取って自然に返答してください。文法的な間違いがあれば、
返答の最後に自然な言い換えを一言だけ添えてください。
```

### スペイン語会話パートナー

```
あなたは初心者向けのスペイン語会話パートナーです。簡単な語彙とゆっくりしたペースの短い文で
話しかけてください。ユーザーのスペルミスや文法の誤りは気にせず意図を汲み取り、会話を優しく
続けてください。必要に応じて、より自然な表現をさりげなく教えてください。
```

> **発展:** 今のままだと1ターンごとに会話がリセットされます。`messages` に過去のやり取りを
> 積み上げていく（会話履歴を持たせる）と、文脈を踏まえたより自然な練習相手になります。

## ローカル RAG（応用）

インターネットを使わずに、手元の PDF やドキュメントを AI に読み込ませる仕組みです。
`PyMuPDF` で PDF を読み込み、Ollama の embeddings モデルで検索エンジンを作ります。

より詳しい解説はこちらの記事もどうぞ。

https://zenn.dev/kazweda/articles/57a9e1d8a32154
