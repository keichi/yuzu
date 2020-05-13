import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import grpc

from .application import Application
from .monitor import Monitor
from .pb.collector_pb2 import TelemetryReply, TimerType
from .pb.collector_pb2_grpc import (YuzuCollectorServicer,
                                    add_YuzuCollectorServicer_to_server)

APP_DEF = [{
    "name": "sim",
    "np": 128,
    "cmd": [
        "/work/keichi/adiosvm/Tutorial/gray-scott/gray-scott",
        "settings-staging.json"
    ],
    "cwd": "/work/keichi/yuzu"
}, {
    "name": "iso",
    "np": 16,
    "cmd": [
        "/work/keichi/adiosvm/Tutorial/gray-scott/isosurface",
        "gs.bp", "iso.bp", "0.5"
    ],
    "cwd": "/work/keichi/yuzu"
}]


class CollectorServicer(YuzuCollectorServicer):
    def __init__(self, apps: Dict[str, Application]):
        self.apps = apps

    def ReportTimer(self, request, context):  # noqa: N802

        app_name = request.common.app_name

        if app_name not in self.apps:
            print(f"Received timer telemetry from unknown app {app_name}")
            return TelemetryReply()

        app = self.apps[app_name]

        if request.timer_type == TimerType.READ_IO:
            app.time_read[request.common.step] = request.duration
        elif request.timer_type == TimerType.COMPUTE:
            app.time_compute[request.common.step] = request.duration
        elif request.timer_type == TimerType.WRITE_IO:
            app.time_write[request.common.step] = request.duration
        elif request.timer_type == TimerType.TOTAL:
            app.time_total[request.common.step] = request.duration
        else:
            print(f"Unknown timer type {request.timer_type}")

        return TelemetryReply()

    def ReportDataSize(self, request, context):  # noqa: N802
        return TelemetryReply()


def main() -> None:
    job_id = os.getenv("JOB_ID")

    print(f"Starting job ID {job_id}")

    master = os.getenv("HOSTNAME")
    print(f"Yuzu master is running on {master}")

    hosts = []
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

    for app_def in APP_DEF:
        monitor.launch(app_def)

    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_YuzuCollectorServicer_to_server(CollectorServicer(monitor.apps),
                                        server)

    print("Starting gRPC server")

    server.add_insecure_port("[::]:50051")
    server.start()

    monitor.wait()

    for name, app in monitor.apps.items():
        print(name, app.time_compute)

    print(f"Exiting job ID {job_id}")


if __name__ == "__main__":
    main()
