import subprocess

def run(domain: str) -> dict:
    """
    Runs Metagoofil to gather documents and extract metadata from the given domain.
    """
    try:
        # Example usage with default flags
        cmd = [
            "python", "metagoofil.py",
            "-d", domain,
            "-t", "pdf,doc,xls,ppt",
            "-l", "50",          # limit of results
            "-n", "5",           # number of files to download
            "-o", "metagoofil_results",
            "-f", "results.html"
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return {
            "module": "Metagoofil",
            "domain": domain,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "Metagoofil",
            "domain": domain,
            "error": e.output.decode("utf-8")
        }
