import json
from pathlib import Path
from typing import Any


class BehavioralMemoryStore:
    def load(self, file_path: str) -> Any:
        return json.loads(Path(file_path).read_text(encoding="utf-8"))
