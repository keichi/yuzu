import os

from .collector import create_collector, start_collector
from .monitor import Monitor

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

    collector = create_collector(monitor.apps)
    start_collector(collector)

    monitor.wait()

    for name, app in monitor.apps.items():
        print(name, app.time_compute)

    print(f"Exiting job ID {job_id}")


if __name__ == "__main__":
    main()
