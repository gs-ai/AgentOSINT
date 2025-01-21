import argparse
import sys
import os

from agentosint.core.module_registry import (
    holehe_module,
    infoga_module,
    sn0int_module,
    whatsmyname_module,
    creepy_module,
    phoneinfoga_module,
    tidos_module,
    massdns_module,
    metagoofil_module,
    scrapling_module,           # NEW
    dorkscraper_module,         # NEW
    breacheddatascraper_module, # NEW
    xnldorker_module,           # NEW
    waymore_module,             # NEW
    camoufox_module             # NEW
)
from agentosint.core.pipeline import Pipeline, PipelineStep

MODULE_MAP = {
    "holehe": holehe_module,
    "infoga": infoga_module,
    "sn0int": sn0int_module,
    "whatsmyname": whatsmyname_module,
    "creepy": creepy_module,
    "phoneinfoga": phoneinfoga_module,
    "tidos": tidos_module,
    "massdns": massdns_module,
    "metagoofil": metagoofil_module,
    "scrapling": scrapling_module,
    "dorkscraper": dorkscraper_module,
    "breacheddatascraper": breacheddatascraper_module,
    "xnldorker": xnldorker_module,
    "waymore": waymore_module,
    "camoufox": camoufox_module
}

def main():
    print("=== AgentOSINT Interactive ===")
    subject_info = input(
        "Enter subject info (comma-separated) \n"
        "e.g. \"Name=John Doe, Email=john.doe@example.com, phone=555-1234\" \n"
        "> "
    )

    name = "Unknown"
    data_pairs = subject_info.split(",")
    parsed_info = {}

    for pair in data_pairs:
        pair = pair.strip()
        if "=" in pair:
            key, value = pair.split("=", 1)
            key = key.strip()
            value = value.strip()
            parsed_info[key.lower()] = value
            if key.lower() == "name":
                name = value

    sanitized_name = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    if not sanitized_name:
        sanitized_name = "Subject"

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    report_filename = f"{sanitized_name}_report.txt"
    report_filepath = os.path.join(desktop_path, report_filename)

    pipeline_steps = []

    email = parsed_info.get("email")
    if email and "holehe" in MODULE_MAP:
        pipeline_steps.append(PipelineStep("holehe", email))

    phone = parsed_info.get("phone")
    if phone and "phoneinfoga" in MODULE_MAP:
        pipeline_steps.append(PipelineStep("phoneinfoga", phone))

    domain = parsed_info.get("domain") or parsed_info.get("website")
    if domain and "massdns" in MODULE_MAP:
        pipeline_steps.append(PipelineStep("massdns", domain))

    pipeline = Pipeline(pipeline_steps)
    pipeline.run()

    results = pipeline.results
    output_lines = [
        f"Subject Name: {name}",
        f"Raw Input: {subject_info}",
        ""
    ]

    for res in results:
        mod_name = res.get("module", "UnknownModule")
        output_lines.append(f"--- Module: {mod_name} ---")
        if "error" in res:
            output_lines.append(f"Error: {res['error']}")
        else:
            output_lines.append(str(res))
        output_lines.append("")

    try:
        with open(report_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))

        print(f"\nReport saved to: {report_filepath}")
    except Exception as e:
        print(f"Could not write report to {report_filepath}: {e}")

if __name__ == "__main__":
    main()
