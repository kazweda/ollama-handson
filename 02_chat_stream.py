import ollama

print("AIとの対話を開始します（Ctrl+Cで終了）")
model_name = 'gemma2:2b'

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
