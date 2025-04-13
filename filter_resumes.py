import os
import shutil

from dotenv import load_dotenv


def main():
    resumes_path = str(os.getenv("RESUMES_PATH"))
    files_name = os.listdir(resumes_path)
    destination = "./resumes/filtered"

    if os.path.isdir(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    for file_name in files_name:
        if not file_name.endswith(".txt"):
            continue

        name = file_name[0:-4]

        with open(
            os.path.join(resumes_path, file_name), "r", encoding="windows-1252"
        ) as file:
            content = file.read().replace("\n", ",")

        with open(
            os.path.join(resumes_path, name + ".lab"), "r", encoding="windows-1252"
        ) as file:
            label = file.read().replace("\n", ",")

        if len(content) > 0 and len(label) > 0:
            shutil.copy(resumes_path + "/" + file_name, destination)
            shutil.copy(resumes_path + "/" + name + ".lab", destination)
        else:
            print(file_name, len(label), len(content))


if __name__ == "__main__":
    load_dotenv()
    main()
