import subprocess
from typing import Dict, List, Optional, Set


class Application:
    def __init__(self, app_def: Dict):
        self.name: str = app_def["name"]
        self.np: int = app_def["np"]
        self.cmd: List[str] = app_def["cmd"]
        self.cwd: str = app_def["cwd"]
        self.nhosts: int = 0
        self.hosts: Set[str] = set()
        self.proc: Optional[subprocess.Popen] = None

        self.time_read: List[float] = []
        self.time_compute: List[float] = []
        self.time_write: List[float] = []
