import subprocess
from typing import Tuple


def run_command(
    command: str, shell: bool = False, timeout: int = 60
) -> Tuple[str, str]:
    args = command.split()
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell,
            timeout=timeout,
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)
