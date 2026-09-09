from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_embeddings(self, texts):
        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
        )

        return embeddings
