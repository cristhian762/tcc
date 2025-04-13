import os
import openai
import time

from dotenv import load_dotenv


def sambanova(resume):
    client = openai.OpenAI(
        api_key=os.getenv("SAMBANOVA_API_KEY"),
        base_url="https://api.sambanova.ai/v1",
    )

    max = int(len(resume) / 2)

    prompt = f"""
        Considering you are an expert in resume summarization. You mainly maintain data related
        to the category of this resume such as Database Administrator, Software Developer, Systems Administrator,
        Project manager, Security Analyst, Web Developer, Network Administrator, Front End Developer, Java Developer 
        and Python Developer for example. 
        Answer objectively with the least amount of characters possible, respecting the maximum of {max} characters.
    """

    response = client.chat.completions.create(
        model="Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": resume},
        ],
        temperature=0.1,
        top_p=0.1,
    )

    return response.choices[0].message.content


def main():
    path = "./resumes/filtered/"
    save_in = "./resumes/llm/"
    files_name = os.listdir(path)
    processed = os.listdir(save_in)

    for file_name in files_name:
        if not file_name.endswith(".txt"):
            continue

        if file_name in processed:
            continue

        with open(os.path.join(path, file_name), "r", encoding="windows-1252") as file:
            content = file.read().replace("\n", ",")

        result = sambanova(content)

        with open(os.path.join(save_in, file_name), "w", encoding="utf-8") as file:
            file.write(str(result))


if __name__ == "__main__":
    load_dotenv()
    main()
