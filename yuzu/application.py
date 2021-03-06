import subprocess
from typing import Dict, List, Optional, Set


class Application:
    def __init__(self, app_def: Dict):
        # TODO Move typings to class body
        self.name: str = app_def["name"]
        self.np: int = app_def["np"]
        self.cmd: List[str] = app_def["cmd"]
        self.cwd: str = app_def["cwd"]
        self.nhosts: int = 0
        self.hosts: Set[str] = set()
        self.proc: Optional[subprocess.Popen] = None

        self.time_read: Dict[int, float] = {}
        self.time_compute: Dict[int, float] = {}
        self.time_write: Dict[int, float] = {}
        self.time_total: Dict[int, float] = {}
