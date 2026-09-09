import ast
import os


def get_python_metadata(code, file_path):
    """
    Extract functions, classes and imports
    from Python code.
    """
    metadata = {
        "file": os.path.basename(file_path),
        "functions": [],
        "classes": [],
        "imports": [],
    }

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            # Functions
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):

                metadata["functions"].append(node.name)

            # Classes
            elif isinstance(node, ast.ClassDef):

                metadata["classes"].append(node.name)

            # Imports
            elif isinstance(node, ast.Import):

                for alias in node.names:

                    metadata["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:

                    metadata["imports"].append(node.module)

    except SyntaxError:

        pass

    return metadata


def get_file_metadata(code, file_path):
    """
    Return metadata depending on
    the programming language.
    """
    extension = os.path.splitext(file_path)[1]

    metadata = {
        "file": os.path.basename(file_path),
        "path": file_path,
        "language": extension.replace(".", ""),
        "type": "code",
    }

    if extension == ".py":

        python_metadata = get_python_metadata(code, file_path)

        metadata.update(python_metadata)

    return metadata
