# agentosint/modules/xnldorker_module.py

import subprocess
import re

def run(dork: str) -> dict:
    """
    Executes xnldorker to gather search results for a given dork phrase.
    We'll parse the output for 'http' links using a regex, as an example.
    """
    result_data = {
        "module": "xnldorker",
        "dork": dork,
        "status": "ok",
        "found_links": []
    }
    try:
        cmd = ["python", "xnldorker.py", "-q", dork]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        output_str = output.decode("utf-8")

        # Example: parse for URLs in the output
        links = re.findall(r'(https?://[^\s]+)', output_str)
        result_data["found_links"] = links

    except subprocess.CalledProcessError as e:
        result_data["status"] = "error"
        result_data["error"] = e.output.decode("utf-8")

    return result_data
