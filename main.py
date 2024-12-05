import os
import openai

from dotenv import load_dotenv

def sambanova():
    client = openai.OpenAI(
        api_key=os.getenv("SAMBANOVA_API_KEY"),
        base_url="https://api.sambanova.ai/v1",
    )

    response = client.chat.completions.create(
        model="Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        temperature=0.1,
        top_p=0.1,
    )

    print(response.choices[0].message.content)

def create_dictionary_with_labels(path, extenssion, multilabel=True):
    dic = {}

    for file in os.listdir(path):
        if not file.endswith(extenssion):
            continue

        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            content = f.read().replace("\n", ",")

            if not multilabel and content == '':
                continue
            
            if not multilabel and ',' in content:
                continue

            if content not in dic:
                dic[content] = []
            
            dic[content] += [file]

    return dic

def print_dictionary(dic):
    data = []

    for key in dic.keys():
        data.append((len(dic[key]), key))

    data = sorted(data, key=lambda x:x[0])

    for quantity, label in data:
        print("{:4} - {}".format(quantity, label))

    total = sum(item[0] for item in data)
    print("\nTotal: {}".format(total))

def main():
    path = "./resumes"
    extenssion = ".lab"
    dic = create_dictionary_with_labels(path, extenssion, False)

    print_dictionary(dic)

if __name__ == "__main__":
    load_dotenv()
    main()
