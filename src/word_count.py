import sys

def word_count():
    with open("text.txt", "r") as f:
        text = f.read()
    word_count = len(text.split())
    with open("result.txt", "w") as f:
        f.write(str(word_count))
    print(f"Word count: {word_count}")
