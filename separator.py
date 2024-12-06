import os
import shutil
import json
from pathlib import Path
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

def create_dir_with_resumes_by_label(origin, destination, extenssion, multilabel=True):
    if os.path.isdir(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    for file in os.listdir(origin):
        if not file.endswith(extenssion):
            continue

        with open(os.path.join(origin, file), "r", encoding="utf-8") as f:
            content = f.read().replace("\n", ",")

            if content == "":
                continue

            if not multilabel and "," in content:
                continue

            dir = destination + "/" + content

            if not os.path.isdir(dir):
                os.mkdir(dir)

            fileName = os.path.basename(f.name).replace(extenssion, ".txt")

            shutil.copy(origin + "/" + fileName, dir)

def print_dir(path):
    folders = [
        name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))
    ]

    print("\nQuantity resumes/folder created: \n")
    for folder in folders:
        count = sum(
            1
            for name in os.listdir(path + "/" + folder)
            if os.path.isfile(os.path.join(path + "/" + folder, name))
        )
        print(count, folder)

    print()

def get_files_test_names(path):
    data = []
    directory = Path(path)

    file_names = [file for file in directory.rglob("*") if file.is_file()]

    for file in file_names:
        data.append(os.path.basename(file).replace(".txt", ""))

    return data

def separate_to_test(items):
    file_name = "train_test.json"
    ids_train, ids_test = train_test_split(items, test_size=0.8, random_state=42)

    data = {"train": ids_train, "test": ids_test}

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

    print("Dados de treino e teste salvos em: {}".format(file_name))

def main():
    path = "./resumes/original"
    resultPath = "./resumes/resumes_by_label"
    extenssion = ".lab"

    create_dir_with_resumes_by_label(path, resultPath, extenssion, False)
    print_dir(resultPath)

    data = get_files_test_names(resultPath)
    separate_to_test(data)

if __name__ == "__main__":
    load_dotenv()
    main()
