import os

from .monitor import Monitor

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


def main() -> None:
    job_id = os.getenv("JOB_ID")

    print(f"Starting job ID {job_id}")

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

    monitor.launch(GS_DEF)
    monitor.launch(PDF_DEF)

    monitor.wait()

    print(f"Exiting job ID {job_id}")


if __name__ == "__main__":
    main()
