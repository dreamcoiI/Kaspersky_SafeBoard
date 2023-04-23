import sys

def word_count():
    with open("text.txt", "r") as file:
        text = file.read()
    text = re.sub(r'[^\w\s]','',text)
    text = text.lower()
    word_count = len(text.split())
    with open("result.txt", "w") as file:
        file.write(str(word_count))

