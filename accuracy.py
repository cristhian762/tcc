import json
import chromadb

from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer


def main():
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

    dic = {}

    for model_name in model_names:
        print(model_name)

        collection_name = f"collection_{model_name}"
        client = chromadb.PersistentClient(path="./chroma")
        collection = client.get_collection(name=collection_name)

        model = SentenceTransformer(model_name)

        with open("separator_for_test.json", "r", encoding="utf-8") as file:
            test = json.load(file)

        accuracy = 0

        n_results_array = [1, 5, 10, 20, 30]

        for n_results in n_results_array:
            accuracy = 0

            for name in test:
                with open(
                    "resumes/original/" + name + ".txt", "r", encoding="windows-1252"
                ) as file:
                    content = file.read().replace("\n", ",")

                with open(
                    "resumes/original/" + name + ".lab", "r", encoding="windows-1252"
                ) as file:
                    labels = file.read().replace("\n", ",")

                query_embedding = model.encode(
                    [
                        "Considering the following resume, find the one that best matches it. Curriculum: "
                        + content
                    ]
                ).tolist()

                results = collection.query(
                    query_embeddings=query_embedding,
                    n_results=n_results,
                )

                hits = 0

                for label in labels.split(","):
                    metadata = results["metadatas"]

                    if not isinstance(metadata, list):
                        continue

                    for item in metadata[0]:
                        if not isinstance(item, dict):
                            continue

                        if not isinstance(item["label"], str):
                            continue

                        if label in item["label"].split(","):
                            hits += 1

                accuracy += hits / len(labels.split(","))

            total_accuracy = accuracy / len(test) / n_results

            print(
                "Número de resultados {} Acurácia {}".format(n_results, total_accuracy)
            )

            if model_name not in dic.keys():
                dic[model_name] = {}

            dic[model_name][n_results] = total_accuracy

    with open("accuracy.json", "w") as file:
        json.dump(dic, file, indent=2)


if __name__ == "__main__":
    load_dotenv()
    main()
