"""
waymore_module.py
"""

import subprocess

def run(domain: str) -> dict:
    """
    Runs waymore to discover archived endpoints and other data about a domain.
    """
    try:
        # Example usage: python waymore.py --domain example.com
        cmd = ["python", "waymore.py", "--domain", domain]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        return {
            "module": "waymore",
            "domain": domain,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "waymore",
            "domain": domain,
            "error": e.output.decode("utf-8")
        }
