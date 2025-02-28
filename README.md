```markdown
# AgentOSINT

An agent for your OSINT.

AgentOSINT is a Python-based open-source intelligence (OSINT) framework that helps analysts gather, correlate, and visualize data from various public sources. It aims to provide:

- **Modular architecture** for adding new OSINT data-collection modules.
- **Flexible command-line interface** for quick and repeatable data gathering.
- **Scalable design** for integration with other tools and APIs.

---

## Features

- **Modular plugin system**: Easily build or integrate new scrapers and data-collection modules.
- **CLI-based usage**: Simple command-line interface to launch OSINT tasks.
- **Integration**: Hooks for databases and analytics platforms.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/gs-ai/AgentOSINT.git
    cd AgentOSINT
    ```

2. (Optional) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate      # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. (Optional) Install the package locally:
    ```bash
    pip install .
    ```

---

## Usage

After installing, you can run the main script:

```bash
python -m agentosint.core.main --help
```

You should see a help message describing available commands and parameters. Example:

```bash
usage: main.py [-h] [--module MODULE_NAME] [--target TARGET] [--run-pipeline]

AgentOSINT CLI

optional arguments:
  -h, --help           show this help message and exit
  --module MODULE_NAME specify which data-collection module to run
  --target TARGET      define target (e.g., domain, username)
  --run-pipeline       run a predefined OSINT pipeline
```

### Example Command

```bash
python -m agentosint.core.main --module=example_module --target="example.com"
```

This example runs a specific module (`example_module`) on the target (`example.com`). It could return data like WHOIS information or basic reconnaissance.

---

## Advanced Usage: Pipelines

You can define and execute OSINT pipelines to automate multi-step processes. Example pipeline:

```python
from agentosint.core.pipeline import Pipeline, PipelineStep

steps = [
    PipelineStep("massdns", "example.com"),
    PipelineStep("xnldorker", "inurl:login.php"),
    PipelineStep("breacheddatascraper", "john.doe@example.com"),
]
pipeline = Pipeline(steps)
pipeline.run()
print("\n=== Pipeline Results (JSON) ===")
print(pipeline.to_json())
```

Alternatively, use the `--run-pipeline` flag to execute a predefined pipeline.

---

## Modules Overview

| Module                       | Input Type      | Purpose                                                                 | Output Fields                    |
|------------------------------|-----------------|-------------------------------------------------------------------------|----------------------------------|
| `breacheddatascraper_module` | Email           | Extract breached data related to a specific email or domain.            | `breached_accounts`, `status`    |
| `camoufox_module`            | URL             | Scrape data from obfuscated or camouflaged sources.                     | `scraped_data`, `status`         |
| `creepy_module`              | Social Media    | Gather geotagged data and metadata from social media platforms.         | `geodata`, `posts`, `status`     |
| `dorkscraper_module`         | Dork string     | Perform advanced search queries using search engine dorks.              | `found_links`, `status`          |
| `holehe_module`              | Email           | Identify services associated with an email address.                     | `found_accounts`, `status`       |
| `infoga_module`              | Email/Domain    | Collect email headers and metadata for intelligence purposes.           | `emails`, `status`, `errors`     |
| `massdns_module`             | Domain          | Conduct fast DNS enumeration for subdomains.                            | `found_subdomains`, `status`     |
| `metagoofil_module`          | Domain          | Extract metadata from public documents on a target domain.              | `document_data`, `status`        |
| `osintgram_module`           | Instagram User  | OSINT analysis on Instagram profiles.                                   | `profile_data`, `posts`, `status`|
| `phoneinfoga_module`         | Phone Number    | Gather details about a phone number (e.g., carrier, location).          | `phone_info`, `status`           |
| `scrapling_module`           | URL             | Perform undetectable and adaptive web scraping.                         | `scraped_data`, `status`         |
| `sn0int_module`              | Domain/Email    | Collect domain/email intelligence with modular pipelines.               | `intelligence_data`, `status`    |
| `tidos_module`               | Domain/IP       | Perform vulnerability assessment and reconnaissance.                    | `vulnerability_report`, `status` |
| `waymore_module`             | URL             | Find wayback snapshots of a website for archival OSINT.                 | `snapshots`, `status`            |
| `xnldorker_module`           | Dork string     | Advanced dork-based reconnaissance across multiple engines.             | `found_links`, `status`          |


## Docker Instructions

Build and run using Docker:

1. Build the Docker image:
    ```bash
    docker build -t agentosint .
    ```

2. Run the container:
    ```bash
    docker run -it agentosint
    ```

---

## Further Ideas

- **Dynamic Configuration**: Use `pipeline.yaml` or `pipeline.json` for flexible pipeline definitions.
- **Result Correlation**: Store results in SQLite/PostgreSQL for easier analysis.
- **Web Dashboard**: Build a Flask or FastAPI interface for browser-based OSINT tasks.
- **API Key Management**: Securely store keys in `.env` files for modules needing API access.

---

## Legal Disclaimer

Use AgentOSINT responsibly and ensure compliance with all applicable laws. OSINT can raise ethical and legal concerns; consult a professional if unsure.

---

For more information, visit the [GitHub repository](https://github.com/gs-ai/AgentOSINT).
```
