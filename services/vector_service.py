import json
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config.settings import EMBEDDING_MODEL

embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

def load_embeddings(file_path="data/vector_backup/embedding_backup.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    text_embeddings = []
    metadatas = []

    for item in data:
        vector = np.array(item["vector"], dtype=np.float32)
        text_embeddings.append((item["text"], vector))
        metadatas.append(item["metadata"])

    vector_store = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=embedding_model,
        metadatas=metadatas
    )
    return vector_store
