import os
import shutil

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
    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

    print("\nQuantity resumes/Folder created: \n")
    for folder in folders:
        count = sum(1 for name in os.listdir(path + "/" + folder) if os.path.isfile(os.path.join(path + "/" + folder, name)))
        print(count, folder)

    print()

def main():
    path = "./resumes"
    resultPath = "./content"
    extenssion = ".lab"

    create_dir_with_resumes_by_label(path, resultPath, extenssion, False)
    print_dir(resultPath)

if __name__ == "__main__":
    load_dotenv()
    main()
