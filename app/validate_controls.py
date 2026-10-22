import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def read_csv(filename):
    with (DATA_DIR / filename).open(
        "r", newline="", encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))

def main():
    risks = read_csv("risk_register.csv")
    controls = read_csv("control_library.csv")

    risk_ids = {risk["risk_id"] for risk in risks}
    errors = []

    for control in controls:
        linked_risk = control["linked_risk_id"]

        if linked_risk not in risk_ids:
            errors.append(
                f'{control["control_id"]}: '
                f'unknown risk ID {linked_risk}'
            )

    print("GRC CONTROL DATA VALIDATION")
    print("=" * 32)
    print(f"Risks checked: {len(risks)}")
    print(f"Controls checked: {len(controls)}")

    if errors:
        print(f"Validation errors: {len(errors)}")
        for error in errors:
            print(f"- {error}")
    else:
        print("Validation passed: all controls link to existing risks.")

if __name__ == "__main__":
    main()
