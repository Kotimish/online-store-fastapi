import json
from pathlib import Path
from typing import Any


class JSONRepository:
    """Хранилище для работы с json-файлами"""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self) -> list[dict[str, Any]]:
        """Загрузить данные из json-файла"""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text("[]")

        with open(self.file_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        return data

    def save(self, data: list[dict[str, Any]]):
        """Сохранить данные в json-файл"""
        if not self.file_path.exists():
            return
        with open(self.file_path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
