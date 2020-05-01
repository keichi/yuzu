#!/usr/bin/env python

import math
import os
import subprocess
import threading
from typing import List, Set

GS_DEF = {
    "name": "sim",
    "np": 128,
    "cmd": [
        "/work/keichi/adiosvm/Tutorial/gray-scott/gray-scott",
        "settings-staging.json"
    ],
    "cwd": "/work/keichi/elastic-workflow"
}

PDF_DEF = {
    "name": "pdf",
    "np": 16,
    "cmd": [
        "/work/keichi/adiosvm/Tutorial/gray-scott/pdf_calc",
        "gs.bp", "pdf.bp"
    ],
    "cwd": "/work/keichi/elastic-workflow"
}


class Application:
    def __init__(self, app_def):
        self.name: str = app_def["name"]
        self.np: int = app_def["np"]
        self.cmd: List[str] = app_def["cmd"]
        self.cwd: str = app_def["cwd"]
        self.nhosts: int = 0
        self.hosts: Set[str] = set()
        self.proc: subprocess.Popen = None

        self.time_read = []
        self.time_compute = []
        self.time_write = []


class Monitor:
    def __init__(self, hosts: List[str]):
        self.host_pool: Set[str] = set(hosts)
        self.apps: List[Application] = []
        self.threads: List[threading.Thread] = []

    def launch(self, app_def) -> None:
        """ Launch application from a definition """

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

        # Launch shephered thread for this app
        thread = threading.Thread(target=self._shepherd, args=(app,))
        thread.start()

        self.threads.append(thread)

    def _shepherd(self, app: Application):
        """ Monitor and communicate with application """

        if app.proc.stdout:
            for line in app.proc.stdout:
                # Need lock here?
                print(f"[app:{app.name}] {line}", end="", flush=True)

        # At this point the app should have terminated, but just to be sure
        app.proc.wait()

    def wait(self):
        """ Wait for  all applications to finish"""

        for thread in self.threads:
            thread.join()


def main() -> None:
    job_id = os.getenv("JOB_ID")

    print(f"Starting job ID {job_id}")

    hosts: List[str] = []
    with open(os.environ["PE_HOSTFILE"]) as f:
        for line in f:
            fields = line.split()

            # We must extract hostname full FQDN to avoid following error:
            # There are no allocated resources for the application:
            #   /work/keichi/adiosvm/Tutorial/gray-scott/pdf_calc
            # that match the requested mapping:
            host_fqdn = fields[0]
            host = host_fqdn.split(".")[0]
            hosts.append(host)

    print(f"Allocated hosts: {hosts}")

    # TODO Should not hardcode master node
    monitor = Monitor(hosts[1:])

    monitor.launch(GS_DEF)
    monitor.launch(PDF_DEF)

    monitor.wait()

    print(f"Exiting job ID {job_id}")


if __name__ == "__main__":
    main()
