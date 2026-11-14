import argparse

import ollama  # noqa: F401 (TODO実装で使用します)

parser = argparse.ArgumentParser()
parser.add_argument(
    '--model', default='gemma3:1b',
    help='使用するモデル名 (default: gemma3:1b)',
)
args = parser.parse_args()

print(f"AIとの対話を開始します（Ctrl+Cで終了）(モデル: {args.model})")
model_name = args.model

while True:
    user_input = input("\nユーザー: ")
    if not user_input:
        continue

    print("AI: ", end="", flush=True)

    # TODO: ollama.chat() を stream=True で呼び出し、stream に受け取ってください
    # ヒント: messages=[{'role': 'user', 'content': user_input}]
    stream = None

    # TODO: stream から順にチャンクを取り出し、
    #       chunk['message']['content'] を print(..., end='', flush=True) してください
    print()
