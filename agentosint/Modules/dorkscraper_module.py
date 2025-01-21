"""
dorkscraper_module.py
"""

import subprocess

def run(dork: str) -> dict:
    """
    Runs dorkScraper to search for URLs returned by a specific Google Dork.
    Example dork: "inurl:admin.php"
    """
    try:
        # If you have the script "dorkScraper.py" in your PATH or in a known location:
        cmd = ["python", "dorkScraper.py", "-d", dork]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        return {
            "module": "dorkScraper",
            "dork": dork,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "dorkScraper",
            "dork": dork,
            "error": e.output.decode("utf-8")
        }
