import os
import zipfile
import tempfile
import shutil

SUPPORTED_EXTENSIONS = (
    ".py",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".js",
    ".ts",
    ".java",
    ".html",
    ".css",
    ".json",
    ".txt",
    ".md",
)


def extract_zip(uploaded_file):
    """
    Extract an uploaded ZIP file into a temporary directory.
    Returns the path of the extracted directory.
    """
    temp_dir = tempfile.mkdtemp()

    zip_path = os.path.join(temp_dir, "project.zip")

    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    extract_path = os.path.join(temp_dir, "project")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path


def get_code_files(project_path):
    """
    Find all supported code files inside the extracted project.
    """
    code_files = []

    for root, dirs, files in os.walk(project_path):

        # Ignore unnecessary folders
        dirs[:] = [
            d for d in dirs
            if d not in [
                ".git",
                "node_modules",
                "__pycache__",
                ".venv",
                "venv",
            ]
        ]

        for file in files:

            if file.endswith(SUPPORTED_EXTENSIONS):

                file_path = os.path.join(root, file)

                code_files.append(file_path)

    return code_files


def read_file(file_path):
    """
    Read a file safely.
    """
    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as f:

            return f.read()

    except Exception:

        return ""
