import os


def get_file_extension(filename: str) -> str:
    """Получаем разрешение файла"""

    _, extension = os.path.splitext(filename)
    return extension.replace(".", "").lower()
