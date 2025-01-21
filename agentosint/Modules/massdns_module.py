import subprocess
import os

def run(domain: str) -> dict:
    """
    Runs Massdns to enumerate subdomains for the given domain.
    """
    try:
        # Example: massdns -r resolvers.txt -t A -o S domainlist.txt
        # We'll generate a temp file with the domain and pass it in.
        with open("target_domain.txt", "w") as f:
            f.write(domain)

        # Adjust paths and flags as needed
        cmd = [
            "massdns",
            "-r", "resolvers.txt",
            "-t", "A",
            "-o", "S",
            "target_domain.txt"
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return {
            "module": "Massdns",
            "domain": domain,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "Massdns",
            "domain": domain,
            "error": e.output.decode("utf-8")
        }
    finally:
        # Cleanup if needed
        if os.path.exists("target_domain.txt"):
            os.remove("target_domain.txt")
