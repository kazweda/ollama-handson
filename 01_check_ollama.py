import ollama

print("Ollamaに接続中...")
try:
    response = ollama.generate(model='gemma3:1b', prompt='「接続成功です」と一言返してください。')
    print("-" * 20)
    print(response['response'])
    print("-" * 20)
except Exception as e:
    print(f"エラーが発生しました: {e}")
    print("Ollamaアプリが起動しているか確認してください。")
