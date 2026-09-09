def chunk_code(code, metadata, chunk_size=1200, overlap=200):
    """
    Split code into chunks.
    """
    chunks = []

    start = 0
    code_length = len(code)

    while start < code_length:

        end = start + chunk_size

        chunk = code[start:end]

        chunks.append({
            "content": chunk,
            "metadata": metadata.copy(),
        })

        start = end - overlap

    return chunks
