import os
import openai
import json
import shutil

from dotenv import load_dotenv


def sambanova(model, content):
    client = openai.OpenAI(
        api_key=os.getenv("SAMBANOVA_API_KEY"),
        base_url="https://api.sambanova.ai/v1",
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "I want you to act as a resume grader. I will provide a complete summary of a person's work experience and skills, along with a list of job categories. Your task is to determine the most appropriate category for the resume based on the experiences, skills, and responsibilities described. Here is the list of categories: Database_Administrator, Network_Administrator, Project_manager, Security_Analyst, Software_Developer, and Systems_Administrator. The answer should be one and only one category from the ones listed above and no extra characters.",
            },
            {"role": "user", "content": content},
        ],
        temperature=0.1,
        top_p=0.1,
    )

    try:
        result = str(response.choices[0].message.content).replace(" ", "_").lower()
    except Exception as e:
        result = 'undetermined'

    print("{:22} | {}".format(result, model))
    return result


def select_model(models):
    print("Escolha qual modelo usar:\n")

    for key, model in enumerate(models):
        print("{:2} - {}".format(key + 1, model))

    print("{:2} - Todos\n".format(len(models) + 1))

    option = int(input("Modelo: "))

    if 0 < option > len(models):
        return models

    return [models[option - 1]]


def classifier(models):
    base = "./resumes/ia/"
    path = "./train_test.json"

    if os.path.isdir(base):
        shutil.rmtree(base)

    os.mkdir(base)

    if not os.path.exists(path):
        print("É necessário rodar o seperador primeiro.")
        return

    with open(path, "r", encoding="utf-8") as file:
        dic = json.load(file)

    data = dic["test"] + dic["train"]
    for test in data:
        filepath = os.path.join("./resumes/original/", test + ".txt")

        with open(filepath, "r", encoding="windows-1252") as file:
            content = file.read()

        with open("./resumes/original/" + test + ".lab", "r", encoding="utf-8") as file:
            correct_label = file.read()

        print("\n {} ({})".format(test, correct_label))
        for model in models:
            label = sambanova(model, content)

            if len(label) > 32:
                label = "undetermined"

            destination = base + model + "/"

            if not os.path.isdir(destination):
                os.mkdir(destination)

            if not os.path.isdir(destination + label):
                os.mkdir(destination + label)

            shutil.copy("./resumes/original/" + test + ".txt", destination + label)


def avaliation(models):
    origin = "./resumes/resumes_by_label/"

    categories = os.listdir(origin)

    resumes_by_label = {}

    for category in categories:
        resumes_by_label[category] = os.listdir(origin + category)

    resumes_by_model = {}

    for model in models:
        origin_ia = "./resumes/ia/" + model + "/"

        categories = os.listdir(origin_ia)

        resumes_by_model[model] = {}

        for category in categories:
            resumes_by_model[model][category] = os.listdir(origin_ia + category)

    result = {}

    for model in models:
        result[model] = 0

        for category in resumes_by_model[model]:
            for resume in resumes_by_model[model][category]:
                if (
                    category in resumes_by_label
                    and resume in resumes_by_label[category]
                ):
                    result[model] += 1

    with open("result.json", "w") as file:
        json.dump(result, file, indent=4)

    print(result)


def main():
    models = [
        "Meta-Llama-3.1-8B-Instruct",
        "Meta-Llama-3.1-70B-Instruct",
        "Meta-Llama-3.1-8B-Instruct",
        "Meta-Llama-3.2-3B-Instruct",
        "Meta-Llama-3.3-70B-Instruct",
        # "Meta-Llama-3.2-1B-Instruct", Always long answers
        # "Meta-Llama-Guard-3-8B", Error
        # "Qwen2.5-72B-Instruct", Slow
        # "Qwen2.5-Coder-32B-Instruct", Slow
        # "QwQ-32B-Preview", Inefficient
    ]

    selected_models = select_model(models)

    classifier(selected_models)
    avaliation(selected_models)


if __name__ == "__main__":
    load_dotenv()
    main()
