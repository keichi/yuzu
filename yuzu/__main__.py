import os
from concurrent.futures import ThreadPoolExecutor

import grpc

from .monitor import Monitor
from .pb.collector_pb2 import TelemetryReply
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
    "name": "pdf",
    "np": 16,
    "cmd": [
        "/work/keichi/adiosvm/Tutorial/gray-scott/pdf_calc",
        "gs.bp", "pdf.bp"
    ],
    "cwd": "/work/keichi/yuzu"
}]


class CollectorServicer(YuzuCollectorServicer):
    def ReportTimer(self, request, context):  # noqa: N802
        print(f"ReportTimer called: {request}")
        return TelemetryReply()

    def ReportDataSize(self, request, context):  # noqa: N802
        print(f"ReportDataSize called {request}")
        return TelemetryReply()


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_YuzuCollectorServicer_to_server(CollectorServicer(), server)

    print("Starting gRPC server")

    server.add_insecure_port("[::]:50051")
    server.start()


def main() -> None:
    job_id = os.getenv("JOB_ID")

    print(f"Starting job ID {job_id}")

    master = os.getenv("HOSTNAME")
    print(f"Yuzu master is running on {master}")

    serve()

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

    monitor.wait()

    print(f"Exiting job ID {job_id}")


if __name__ == "__main__":
    main()
