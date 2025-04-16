![AgentOSINT Logo](e61a0344-5b20-43a0-867e-b817b36c7c85.png)

# AgentOSINT

An advanced OSINT framework for professionals.

AgentOSINT is a Python-based open-source intelligence (OSINT) framework designed for analysts to efficiently collect, correlate, and visualize data from public sources. It provides:

- **Modular architecture** for seamless addition of OSINT data-collection modules.
- **Command-line interface (CLI)** for streamlined and repeatable data gathering.
- **Scalability** for integration with databases, APIs, and analytics tools.

---

## Features

- **Extensible plugin system**: Easily integrate custom scrapers and data-collection modules.
- **CLI-based execution**: Lightweight and fast OSINT workflows from the terminal.
- **Database integration**: Supports storage and retrieval of intelligence data.
- **Pipeline automation**: Define OSINT workflows for multi-step data collection.

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/gs-ai/AgentOSINT.git
cd AgentOSINT
```

### (Optional) Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate    # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### (Optional) Install the Package Locally
```bash
pip install .
```

---

## Usage

Run the main script with:
```bash
python -m agentosint.core.main --help
```

Example:
```bash
python -m agentosint.core.main --module=whois --target="example.com"
```

This command runs the `whois` module to fetch domain registration details.

---

## OSINT Pipelines

Automate OSINT workflows by defining and executing pipelines:

```python
from agentosint.core.pipeline import Pipeline, PipelineStep

steps = [
    PipelineStep("massdns", "example.com"),
    PipelineStep("breacheddatascraper", "john.doe@example.com"),
]
pipeline = Pipeline(steps)
pipeline.run()
print("\n=== Pipeline Results ===")
print(pipeline.to_json())
```

Alternatively, run pipelines via CLI:
```bash
python -m agentosint.core.main --run-pipeline
```

---

## Supported Modules

| Module               | Input Type     | Purpose                                         |
|----------------------|----------------|-------------------------------------------------|
| `whois_module`       | Domain         | Retrieve WHOIS domain registration info         |
| `breacheddatascraper`| Email          | Extract data from known breaches                |
| `massdns_module`     | Domain         | Conduct DNS subdomain enumeration               |
| `scrapling_module`   | URL            | Adaptive web scraping with stealth techniques   |
| `osintgram_module`   | Instagram User | Social media intelligence on IG profiles        |
| `phoneinfoga_module` | Phone Number   | Gather phone number details (carrier, location) |
| `tidos_module`       | Domain/IP      | Perform vulnerability reconnaissance            |
| `waymore_module`     | URL            | Find archived snapshots of a website            |

---

## Running with Docker

### Build the Image
```bash
docker build -t agentosint .
```

### Run the Container
```bash
docker run -it agentosint
```

---

## Future Enhancements

- **Web Dashboard**: Interactive Flask/FastAPI-based interface.
- **SQLite/PostgreSQL Support**: Persistent data storage for OSINT findings.
- **API Key Management**: Secure handling of API keys for enhanced intelligence gathering.

---

## Legal Disclaimer

Use AgentOSINT responsibly and in compliance with all applicable laws. OSINT must be conducted ethically. Consult legal professionals if unsure.

For more details, visit the [GitHub repository](https://github.com/gs-ai/AgentOSINT).

