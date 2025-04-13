import os
import json
import tiktoken

DIRECTORY_A = "resumes/filtered/"
DIRECTORY_B = "resumes/llm/"
VALID_EXTENSIONS = [".txt"]
OUTPUT_FILE = "token_count.json"

tokenizer = tiktoken.get_encoding("cl100k_base")

token_counts = {
    "filtered": {"tokens": 0, "characters": 0},
    "llm": {"tokens": 0, "characters": 0},
}

for root, dirs, files in os.walk(DIRECTORY_A):
    for filename in files:
        _, ext = os.path.splitext(filename)
        if ext in VALID_EXTENSIONS:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="windows-1252") as f:
                    content = f.read()
                    tokens = tokenizer.encode(content)
                    token_counts["filtered"]["characters"] += len(content)
                    token_counts["filtered"]["tokens"] += len(tokens)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

for root, dirs, files in os.walk(DIRECTORY_B):
    for filename in files:
        _, ext = os.path.splitext(filename)
        if ext in VALID_EXTENSIONS:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    tokens = tokenizer.encode(content)
                    token_counts["llm"]["characters"] += len(content)
                    token_counts["llm"]["tokens"] += len(tokens)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(token_counts, f, indent=4, ensure_ascii=False)

print(token_counts)
