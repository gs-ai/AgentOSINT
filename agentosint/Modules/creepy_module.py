import subprocess

def run(target: str) -> dict:
    """
    Runs Creepy in CLI mode (if available) against the specified target.
    'target' might be a username or social media handle.
    """
    try:
        # The CLI usage for Creepy might vary, so consult the tool’s docs.
        # For demonstration purposes:
        cmd = ["creepy", "--search", target]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return {
            "module": "Creepy",
            "target": target,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "Creepy",
            "target": target,
            "error": e.output.decode("utf-8")
        }
