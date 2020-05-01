import math
import os
import subprocess
import threading
from typing import Dict, List, Set

from .application import Application


class Monitor:
    def __init__(self, hosts: List[str]):
        self.host_pool: Set[str] = set(hosts)
        self.apps: Dict[str, Application] = {}
        self.threads: Dict[str, threading.Thread] = {}

    def launch(self, app_def: Dict) -> None:
        """ Launch an application from a definition """

        app = Application(app_def)

        # TODO Should not hardcode # of cores
        app.nhosts = math.ceil(app.np / 24)

        # TODO Smarter node allocation algorithm?
        for _ in range(app.nhosts):
            app.hosts.add(self.host_pool.pop())

        full_cmd = [
            "mpirun",
            "-x", "MASTER",
            "-x", "APP_NAME",
            "-n", str(app.np),
            "-H", ",".join(app.hosts),
            "--nolocal"
        ] + app.cmd

        # These environment variables will be available from the app
        env = os.environ.copy()
        env["APP_NAME"] = app.name
        env["MASTER"] = os.environ["HOST"]

        print(f"Launching app {app.name}: {full_cmd}", flush=True)

        # Launch app
        app.proc = subprocess.Popen(full_cmd, cwd=app.cwd, env=env,
                                    stdout=subprocess.PIPE, text=True)

        self.apps[app.name] = app

        # Launch shephered thread for this app
        thread = threading.Thread(target=self._shepherd, args=(app,))
        self.threads[app.name] = thread
        thread.start()

    def _shepherd(self, app: Application) -> None:
        """ Monitor and communicate with an application """

        if app.proc is None:
            return

        if app.proc.stdout:
            for line in app.proc.stdout:
                # Need lock here?
                print(f"[app:{app.name}] {line}", end="", flush=True)

        # At this point the app should have terminated, but just to be sure
        app.proc.wait()

    def wait(self) -> None:
        """ Wait for all applications to finish"""

        for thread in self.threads.values():
            thread.join()
