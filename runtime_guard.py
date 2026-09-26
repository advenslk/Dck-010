import os
import shlex


def get_container_runtime_limits():
    return {
        "pids_limit": int(os.getenv("VPS_PIDS_LIMIT", "512")),
    }


def build_secure_docker_run(name: str, hostname: str, image: str) -> str:
    """Build a safer Docker command for user VPS containers.

    This intentionally removes --privileged/--cap-add=ALL from newly created
    VPS containers. Existing containers are not modified by this function.
    """
    q = shlex.quote
    limits = get_container_runtime_limits()
    return (
        f"docker run -d --name {q(name)} --hostname {q(hostname)} "
        f"--security-opt no-new-privileges:true "
        f"--pids-limit {limits['pids_limit']} "
        f"--tmpfs /run --tmpfs /run/lock "
        f"{q(image)} /bin/sh -c 'while true; do sleep 3600; done'"
    )
