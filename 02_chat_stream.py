import argparse
import ollama

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

    # stream=Trueにすることで、生成された文字から順次表示されます
    stream = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': user_input}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    print()
