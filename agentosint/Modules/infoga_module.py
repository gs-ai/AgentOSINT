import subprocess
import os

def run(target: str) -> dict:
    """
    Runs Infoga to gather email info from public sources.
    """
    try:
        # Example CLI usage after cloning Infoga or installing from a local path
        # Usage might vary depending on your Infoga setup
        cmd = ["python", "Infoga.py", "--target", target, "--source", "all", "--breach", "true"]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return {
            "module": "Infoga",
            "target": target,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "Infoga",
            "target": target,
            "error": e.output.decode("utf-8")
        }
