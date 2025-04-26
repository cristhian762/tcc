import json
import openai
import os
import re

from chroma import search_chroma
from dotenv import load_dotenv


def sambanova(query, resumes, model):
    client = openai.OpenAI(
        api_key=os.getenv("SAMBANOVA_API_KEY"),
        base_url="https://api.sambanova.ai/v1",
    )

    content = ""

    for i in range(0, len(resumes["ids"][0])):
        content += "resume_id: " + resumes["ids"][0][i] + "\n"
        content += resumes["documents"][0][i] + "\n\n"
        content += "---\n"

    prompt = """
I will provide you with one base resume and 20 other resumes.
Your task is to compare the 20 resumes to the base resume and identify the 5 most similar ones based on content, skills, 
experience, and overall relevance.

Each resume will have a unique identifier in the format: `resume_id: <ID>`.

At the end, return a JSON object containing only the 5 most similar resume IDs, sorted from most to least similar.

Format the output strictly like this:
{
  "most_similar_resume_ids": ["<ID1>", "<ID2>", "<ID3>", "<ID4>", "<ID5>"]
}

Do not include any explanation, only the JSON response.

Here is the base resume:
---
"""
    prompt += query
    prompt += f"""
---

And here are the 10 other resumes:
---
{content}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in natural language processing and resume analysis. "
                    "Your task is to compare resumes and return only the most relevant ones in JSON format, "
                    "based strictly on the user's instructions."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        top_p=0.1,
    )

    try:
        return response.choices[0].message.content
    except Exception as e:
        print("Resposta inválida")
        print(response)
        return ""


def main():
    models = [
        "Meta-Llama-3.2-1B-Instruct",
        "Meta-Llama-3.1-8B-Instruct",
        "Meta-Llama-3.3-70B-Instruct",
        "Llama-4-Scout-17B-16E-Instruct",
    ]

    with open("separator_for_test.json", "r", encoding="utf-8") as file:
        test = json.load(file)

    if not os.path.isfile("sambanova_results.json"):
        with open("sambanova_results.json", "w", encoding="utf-8") as file:
            json.dump({}, file, indent=2)

    with open("sambanova_results.json", "r", encoding="utf-8") as file:
        sambanova_results = json.load(file)

    for model in models:
        print(f"Analisando com modelo {model}")

        for name in test:
            if (
                model in sambanova_results
                and name in sambanova_results[model]
                and sambanova_results[model][name][0] != "limit tokens"
            ):
                continue

            print(f"Analisando currículo {name}")

            with open(
                "resumes/original/" + name + ".txt", "r", encoding="windows-1252"
            ) as file:
                content = file.read().replace("\n", ",")

            chromadb = search_chroma(content, 10)

            if model not in sambanova_results.keys():
                sambanova_results[model] = {}

            try:
                result = sambanova(
                    content,
                    {"ids": chromadb["ids"], "documents": chromadb["documents"]},
                    model,
                )
            except Exception as e:
                print(e)
                print(f"O currículo {name} atingiu o limite de tokens")
                sambanova_results[model][name] = ["limit tokens"]

                with open("sambanova_results.json", "w", encoding="utf-8") as file:
                    json.dump(sambanova_results, file, indent=2)

                continue

            if not result:
                continue

            match = re.search(r"{(.|\n)*?}", result)

            if match:
                result = match.group(0)

            try:
                result = json.loads(result)
            except Exception as e:
                print(f"O currículo {name} não teve um json como resposta")
                sambanova_results[model][name] = ["json invalid"]

                with open("sambanova_results.json", "w", encoding="utf-8") as file:
                    json.dump(sambanova_results, file, indent=2)

                continue

            if not isinstance(result, dict) or "most_similar_resume_ids" not in result:
                continue

            sambanova_results[model][name] = result["most_similar_resume_ids"]

            with open("sambanova_results.json", "w", encoding="utf-8") as file:
                json.dump(sambanova_results, file, indent=2)


if __name__ == "__main__":
    load_dotenv()
    main()
