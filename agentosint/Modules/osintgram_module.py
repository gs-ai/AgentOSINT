import subprocess

def run(username: str) -> dict:
    """
    Runs Osintgram to gather data about an Instagram username.
    """
    try:
        cmd = ["python3", "main.py", username]
        # You might also pass commands to list followers, following, etc.
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return {
            "module": "Osintgram",
            "target": username,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "Osintgram",
            "target": username,
            "error": e.output.decode("utf-8")
        }
