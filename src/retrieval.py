def retrieve_code(question, embedding_model, vector_store, k=5):
    """
    Retrieve relevant code chunks
    for the user's question.
    """
    query_embedding = embedding_model.create_embeddings([question])[0]

    results = vector_store.search(query_embedding, k)

    return results
