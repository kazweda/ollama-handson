import argparse
import ollama

parser = argparse.ArgumentParser()
parser.add_argument('image', help='画像ファイルのパス')
parser.add_argument(
    '--model', default='gemma3:4b',
    help='使用するモデル名 (default: gemma3:4b)',
)
parser.add_argument(
    '--prompt',
    default='この画像を日本語で説明してください。',
    help='プロンプト',
)
args = parser.parse_args()

print(f"画像を解析中... (モデル: {args.model})")
try:
    response = ollama.chat(
        model=args.model,
        messages=[{
            'role': 'user',
            'content': args.prompt,
            'images': [args.image],
        }],
    )
    print("-" * 20)
    print(response['message']['content'])
    print("-" * 20)
except Exception as e:
    print(f"エラーが発生しました: {e}")
    print("モデルがvisionに対応しているか確認してください: ollama show モデル名")
