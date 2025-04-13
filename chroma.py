import chromadb

from sentence_transformers import SentenceTransformer


def search_chroma(query, n_results, model_name="multi-qa-MiniLM-L6-cos-v1"):
    collection_name = f"collection_{model_name}"
    client = chromadb.PersistentClient(path="./chroma")
    collection = client.get_collection(name=collection_name)

    model = SentenceTransformer(model_name)

    query_embedding = model.encode(
        [
            "Considering the following resume, find the one that best matches it. Curriculum: "
            + query
        ]
    ).tolist()

    return collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )
