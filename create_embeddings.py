import json
import os
import chromadb
import random

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


def separator_for_test():
    print("Garanta que não há problemas em sobrescrever o resumes by label")
    return
    with open("resumes_by_label.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    test = []

    for label in data.keys():
        resumes = data[label]

        test += random.sample(resumes, 100)

    with open("separator_for_test.json", "w") as file:
        json.dump(test, file, indent=2)


def collection_add(collection, model_name):
    print("Start Collection add {}".format(model_name))
    model = SentenceTransformer(model_name)
    embedding_dim = model.get_sentence_embedding_dimension()

    if collection.metadata and "embedding_dim" in collection.metadata:
        if collection.metadata["embedding_dim"] != embedding_dim:
            print(f"⚠️ Dimensão incompatível para {model_name}!")
            exit()
    else:
        collection.metadata = {"embedding_dim": embedding_dim}

    if not os.path.isfile("separator_for_test.json"):
        separator_for_test()

    if "RESUMES_PATH" not in os.environ:
        print("RESUMES_PATH undefined")
        exit()

    with open("separator_for_test.json", "r", encoding="utf-8") as file:
        test = json.load(file)

    resumes_path = "./resumes/pegasus/"
    files_name = os.listdir(resumes_path)

    ids = []
    metadatas = []
    documents = []

    for file_name in files_name:
        if not file_name.endswith(".txt"):
            continue

        name = file_name[0:-4]

        if name in test:
            continue

        with open(os.path.join(resumes_path, file_name), "r", encoding="utf-8") as file:
            content = file.read().replace("\n", ",")

        with open(
            os.path.join(resumes_path, name + ".lab"), "r", encoding="windows-1252"
        ) as file:
            label = file.read().replace("\n", ",")

        ids.append(name)
        metadatas.append({"file_name": file_name, "label": label})
        documents.append(content)

    embeddings = model.encode(documents).tolist()

    assert len(embeddings[0]) == embedding_dim, "Dimensão do embedding não bate!"

    collection.upsert(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )


def resumes_by_label():
    path = "./resumes/filtered/"
    dic = {}

    for file in os.listdir(path):
        if not file.endswith(".lab"):
            continue

        with open(os.path.join(path, file), "r", encoding="windows-1252") as f:
            labels = f.read().replace("\n", ",")

        for label in labels.split(","):
            if label not in dic:
                dic[label] = []

            dic[label] += [file[:-4]]

    with open("resumes_by_label.json", "w", encoding="utf-8") as file:
        json.dump(dic, file, ensure_ascii=False, indent=4)


def main():
    # resumes_by_label()

    model_names = [
        "all-mpnet-base-v2",
        "multi-qa-mpnet-base-dot-v1",
        "all-distilroberta-v1",
        "all-MiniLM-L12-v2",
        "multi-qa-distilbert-cos-v1",
        "all-MiniLM-L6-v2",
        "multi-qa-MiniLM-L6-cos-v1",
        "paraphrase-multilingual-mpnet-base-v2",
        "paraphrase-albert-small-v2",
        "paraphrase-multilingual-MiniLM-L12-v2",
        "paraphrase-MiniLM-L3-v2",
        "distiluse-base-multilingual-cased-v1",
        "distiluse-base-multilingual-cased-v2",
    ]

    for model_name in model_names:
        client = chromadb.PersistentClient(path="./chroma/")

        collection_name = f"collection_{model_name}"

        model = SentenceTransformer(model_name)
        embedding_dim = model.get_sentence_embedding_dimension()

        collection = client.get_or_create_collection(
            name=collection_name, metadata={"embedding_dim": embedding_dim}
        )

        collection_add(collection, model_name)


if __name__ == "__main__":
    load_dotenv()
    main()
