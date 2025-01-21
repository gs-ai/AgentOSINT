import subprocess

def run(target: str) -> dict:
    """
    Runs TIDoS to enumerate the given target (domain/IP).
    """
    try:
        # TIDoS can be interactive. For automated usage, you might have to script inputs
        # or rely on any "headless" flags it might provide.
        cmd = ["python", "tidos.py", "-u", target, "--scan", "recon"]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return {
            "module": "TIDoS",
            "target": target,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "TIDoS",
            "target": target,
            "error": e.output.decode("utf-8")
        }
