from pathlib import Path
import json


class JsonStorage:
    def __init__(self, json_path: str = None) -> None:
        if json_path is None:
            self.json_path = Path(__file__).resolve().parent / "data.json"
        else:
            self.json_path = Path(json_path)

        if self.json_path.is_dir() or self.json_path.suffix.lower() != ".json":
            self.json_path = self.json_path / "data.json"

    def read_json(self) -> dict:
        if not self.json_path.is_file() or self.json_path.stat().st_size == 0:
            return {}
        try:
            with open(self.json_path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            return {}

    def write_json(self, data: dict) -> None:
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
