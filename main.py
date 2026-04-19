import os
import sys
import csv

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from attacker.payloads import payloads
from defender.input_validator import validate_input
from defender.prompt_separator import build_safe_prompt
from defender.guardrail import check_output
from attacker.attacker import send_payload

LOG_FILE = "logs/results.csv"


def run_defended_test():
    print("Starting defended prompt injection tests...\n")

    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Category",
            "Payload",
            "Validator Result",
            "Model Response",
            "Guardrail Status",
            "Guardrail Reason"
        ])

    for item in payloads:
        category = item["category"]
        prompt = item["prompt"]

        print(f"[{category}] Testing payload...")

        validation = validate_input(prompt)

        if not validation["safe"]:
            print(f"BLOCKED by validator: {validation['reason']}\n")
            with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    category,
                    prompt,
                    f"BLOCKED: {validation['reason']}",
                    "N/A",
                    "N/A",
                    "N/A"
                ])
            continue

        safe_prompt = build_safe_prompt(prompt)
        model_response = send_payload(safe_prompt["messages"][0]["content"])

        guardrail = check_output(prompt, model_response)

        print(f"Validator: PASSED")
        print(f"Model Response: {model_response[:100]}...")
        print(f"Guardrail: {guardrail['status']} — {guardrail['reason']}\n")

        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                category,
                prompt,
                "PASSED",
                model_response,
                guardrail["status"],
                guardrail["reason"]
            ])

    print("Testing complete. Results saved to logs/results.csv")


if __name__ == "__main__":
    run_defended_test()