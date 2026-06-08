import json
from pathlib import Path


class RealDataLoader:
    def load_json(self, file_path):
        return json.loads(Path(file_path).read_text(encoding="utf-8"))
