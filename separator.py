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


def print_dictionary(dic):
    data = []

    for key in dic.keys():
        data.append((len(dic[key]), key))

    data = sorted(data, key=lambda x: x[0])

    for quantity, label in data:
        print("{:4} - {}".format(quantity, label))

    total = sum(item[0] for item in data)
    print("\nTotal: {}".format(total))


def main():
    path = "./resumes"
    resultPath = "./content"
    extenssion = ".lab"

    create_dir_with_resumes_by_label(path, resultPath, extenssion, False)


if __name__ == "__main__":
    load_dotenv()
    main()
