import subprocess

def run(phone_number: str) -> dict:
    """
    Runs PhoneInfoga on the given phone number.
    """
    try:
        # CLI usage: phoneinfoga scan --number <phone_number>
        cmd = ["phoneinfoga", "scan", "--number", phone_number]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return {
            "module": "PhoneInfoga",
            "target": phone_number,
            "raw_output": output.decode("utf-8")
        }
    except subprocess.CalledProcessError as e:
        return {
            "module": "PhoneInfoga",
            "target": phone_number,
            "error": e.output.decode("utf-8")
        }
