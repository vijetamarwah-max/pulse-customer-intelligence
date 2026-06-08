from copy import deepcopy
from typing import Dict, Optional


class WorkspaceStore:
    """Small in-memory workspace store for the hosted prototype.

    Production should replace this with Postgres plus object storage for source files.
    """

    def __init__(self) -> None:
        self._workspaces: Dict[str, Dict] = {}

    def save(self, workspace_id: str, payload: Dict, computed: Dict) -> None:
        self._workspaces[workspace_id] = {
            "payload": deepcopy(payload),
            "computed": deepcopy(computed),
        }

    def get(self, workspace_id: str = "default") -> Optional[Dict]:
        workspace = self._workspaces.get(workspace_id)
        if not workspace:
            return None

        return deepcopy(workspace)

    def has_data(self, workspace_id: str = "default") -> bool:
        return workspace_id in self._workspaces
