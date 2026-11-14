import argparse

import ollama

parser = argparse.ArgumentParser()
parser.add_argument(
    '--model', default='gemma3:1b',
    help='使用するモデル名 (default: gemma3:1b)',
)
args = parser.parse_args()

print(f"Ollamaに接続中... (モデル: {args.model})")
try:
    response = ollama.generate(
        model=args.model,
        prompt='「接続成功です」と一言返してください。',
    )
    print("-" * 20)
    print(response['response'])
    print("-" * 20)
except Exception as e:  # noqa: BLE001 (ハンズオン用に全エラーを捕捉)
    print(f"エラーが発生しました: {e}")
    print("Ollamaアプリが起動しているか確認してください。")
