import os
import re
import chromadb

from dotenv import load_dotenv


def exemple():
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="tutorial_collection")

    collection.add(
        documents=[
            "É um documento sobre machine learning",
            "É outro documento sobre data science",
            "É parte de um documento sobre artificial intelligence",
        ],
        metadatas=[
            {"source": "tutorial1"},
            {"source": "tutorial2"},
            {"source": "tutorial3"},
        ],
        ids=["id1", "id2", "id3"],
    )

    results = collection.query(
        query_texts=["Eu gostaria de saber algo sobre artificial intelligence"],
        n_results=2,
    )

    print(results)


def collection_add(collection):
    if "RESUMES_PATH" not in os.environ:
        print("RESUMES_PATH undefined")
        exit()

    resumes_path = str(os.getenv("RESUMES_PATH"))
    files_name = os.listdir(resumes_path)

    ids = []
    metadatas = []
    documents = []

    for file_name in files_name:
        if not file_name.endswith(".txt"):
            continue

        name = file_name[0:-4]

        with open(
            os.path.join(resumes_path, file_name), "r", encoding="windows-1252"
        ) as file:
            content = file.read().replace("\n", ",")

        ids.append(name)
        metadatas.append({"file_name": file_name})
        documents.append(content)

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )


def main():
    collection_name = "all_resumes_data"

    client = chromadb.PersistentClient(path="./chroma")
    collections = client.list_collections()
    collection = client.get_or_create_collection(name=collection_name)

    if collection_name not in collections:
        print("Adicionando currículos ao chromadb ...")
        collection_add(collection)
    else:
        print("Coleção encontrada")

    results = collection.query(
        query_texts=["Which one has the most experience with Database Administrator?"],
        n_results=2,
    )

    print(results)


if __name__ == "__main__":
    load_dotenv()
    main()
