from pathlib import Path
import json


class JsonStorage:
    """
    A class for handling JSON file storage.

    This class allows creating an object that works with a JSON file.
    It can read from and write to the JSON file specified by the user or use a default file.
    """

    def __init__(self, json_path: str = None) -> None:
        """
            Initializes a JsonStorage object. The object accepts an optional parameter json_path — the path to a JSON file. If the path is not provided or does not exist, the object's json_path attribute is set to the default path data.json.
            :param json_path: str | None
        Path to the JSON file. If None, defaults to "data.json".
        """
        if json_path is None:
            self.json_path = Path(__file__).resolve().parent / "data.json"
        else:
            self.json_path = Path(json_path)

        if self.json_path.is_dir() or self.json_path.suffix.lower() != ".json":
            self.json_path = self.json_path / "data.json"

    def read_json(self) -> dict:
        """
        Reads data from the JSON file specified by the object's path.

        Checks whether the file exists and is not empty.
        If the file exists and contains valid JSON data, returns it as a dictionary.
        If the file does not exist, is empty, or contains invalid JSON, returns an empty dictionary.

        :return: dict
            The JSON data as a dictionary, or an empty dictionary if the file is missing, empty, or invalid.
        """
        if not self.json_path.is_file() or self.json_path.stat().st_size == 0:
            return {}
        try:
            with open(self.json_path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            return {}

    def write_json(self, data: dict) -> None:
        """
        Writes the provided data to the JSON file specified by the object's path.

        Ensures that the parent directories exist, creating them if necessary.
        The data is written in JSON format with UTF-8 encoding, without ASCII escaping,
        and with an indentation of 4 spaces.

        :param data: dict
            The dictionary to be written to the JSON file.
        :return: None
        """
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
