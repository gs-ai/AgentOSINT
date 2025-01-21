import subprocess
import logging
import json
from typing import Dict, Union

def setup_logging():
    """
    Sets up logging configuration for the module with both file and console outputs.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("beefed_data_scraper.log"),
            logging.StreamHandler()
        ]
    )

setup_logging()

def parse_output(raw_output: str) -> Union[dict, str]:
    """
    Attempts to parse the raw output as JSON. If parsing fails, returns the raw output.

    Args:
        raw_output (str): The raw output string from the subprocess command.

    Returns:
        dict or str: Parsed JSON object if successful, else raw output string.
    """
    try:
        parsed = json.loads(raw_output)
        logging.debug("Successfully parsed raw output to JSON.")
        return parsed
    except json.JSONDecodeError:
        logging.warning("Raw output is not valid JSON. Returning as string.")
        return raw_output

def run(query: str) -> Dict[str, Union[str, dict]]:
    """
    Executes BeefedDataScraper with the given query and processes the results.

    Args:
        query (str): The query string (email, username, or phone) to search for.

    Returns:
        dict: Contains the module name, query, raw output, parsed output, and errors if any.
    """
    logging.info(f"Initiating BeefedDataScraper for query: {query}")

    try:
        cmd = ["python", "BDS.py", "--query", query]
        logging.debug(f"Running command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        raw_output = result.stdout.strip()
        parsed_output = parse_output(raw_output)

        logging.info("BeefedDataScraper completed successfully.")
        return {
            "module": "BeefedDataScraper",
            "query": query,
            "raw_output": raw_output,
            "parsed_output": parsed_output
        }

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        logging.error(f"Command failed with error: {error_message}")
        return {
            "module": "BeefedDataScraper",
            "query": query,
            "error": error_message
        }

    except Exception as ex:
        logging.exception("Unexpected error occurred.")
        return {
            "module": "BeefedDataScraper",
            "query": query,
            "error": str(ex)
        }

def save_to_file(data: Dict[str, Union[str, dict]], filename: str = "output.json"):
    """
    Saves the result data to a JSON file.

    Args:
        data (dict): The data to save.
        filename (str): The file name to save the data into.
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Results successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to file: {e}")

if __name__ == "__main__":
    # Example for testing the module functionality
    test_query = "example@example.com"
    result = run(test_query)
    logging.debug(f"Run result: {result}")

    save_to_file(result, "beefed_data_result.json")
    print("Results saved to beefed_data_result.json")
