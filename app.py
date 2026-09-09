import streamlit as st
from dotenv import load_dotenv

from src.file_handler import (
    extract_zip,
    get_code_files,
    read_file,
)

from src.code_parser import (
    get_file_metadata,
)

from src.chunker import (
    chunk_code,
)

from src.embeddings import (
    EmbeddingModel,
)

from src.vector_store import (
    FAISSVectorStore,
)

from src.retrieval import (
    retrieve_code,
)

from src.groq_llm import (
    GroqLLM,
)

from src.prompts import (
    create_code_prompt,
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CodeMind AI",
    page_icon="🤖",
    layout="wide",
)

# Title
st.title("🤖 CodeMind AI")

st.write(
    "An AI-powered Codebase Intelligence "
    "Assistant using RAG."
)

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "embedding_model" not in st.session_state:
    st.session_state.embedding_model = None

if "project_analyzed" not in st.session_state:
    st.session_state.project_analyzed = False

# Sidebar
with st.sidebar:
    st.header("📂 Upload Project")

    uploaded_file = st.file_uploader(
        "Upload your project ZIP file",
        type=["zip"],
    )

# Analyze project
if uploaded_file and not st.session_state.project_analyzed:

    if st.button("🚀 Analyze Project"):

        with st.spinner("Analyzing your codebase..."):

            # Extract project
            project_path = extract_zip(uploaded_file)

            # Find code files
            code_files = get_code_files(project_path)

            all_chunks = []

            # Process files
            for file_path in code_files:

                code = read_file(file_path)

                if not code.strip():
                    continue

                metadata = get_file_metadata(code, file_path)

                chunks = chunk_code(code, metadata)

                all_chunks.extend(chunks)

            # Check chunks
            if not all_chunks:
                st.error("No supported code files found.")
                st.stop()

            # Create embedding model
            embedding_model = EmbeddingModel()

            # Prepare texts
            texts = [chunk["content"] for chunk in all_chunks]

            # Create embeddings
            embeddings = embedding_model.create_embeddings(texts)

            # Create FAISS DB
            vector_store = FAISSVectorStore()

            vector_store.create_index(embeddings, all_chunks)

            # Save in session
            st.session_state.vector_store = vector_store
            st.session_state.embedding_model = embedding_model
            st.session_state.project_analyzed = True

        st.success(
            f"Project analyzed successfully! "
            f"Found {len(code_files)} files "
            f"and created {len(all_chunks)} "
            f"code chunks."
        )

# Chat Section
if st.session_state.project_analyzed:

    st.divider()

    st.subheader("💬 Ask About Your Code")

    question = st.chat_input("Ask a question about the project...")

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("CodeMind AI is thinking..."):

                # Retrieve relevant code
                results = retrieve_code(
                    question,
                    st.session_state.embedding_model,
                    st.session_state.vector_store,
                )

                # Create context
                context_parts = []

                for result in results:

                    file_name = result["metadata"].get("file", "Unknown")

                    content = result["content"]

                    context_parts.append(
                        f"FILE:\n{file_name}\n\nCODE:\n\n{content}"
                    )

                context = "\n\n".join(context_parts)

                # Create prompt
                prompt = create_code_prompt(question, context)

                # Generate answer
                try:
                    llm = GroqLLM()

                    answer = llm.generate_answer(prompt)

                    st.write(answer)

                    # Show sources
                    st.subheader("📌 Relevant Sources")

                    source_files = set()

                    for result in results:
                        source_files.add(
                            result["metadata"].get("file", "Unknown")
                        )

                    for file in source_files:
                        st.write(f"📄 {file}")

                except Exception as e:
                    st.error(f"Groq Error: {str(e)}")
