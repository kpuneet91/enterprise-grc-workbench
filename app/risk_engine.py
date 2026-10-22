import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RISK_FILE = PROJECT_ROOT / "data" / "risk_register.csv"


def calculate_risk_score(likelihood, impact):
    """Calculate a simple inherent risk score from likelihood and impact."""
    likelihood = int(likelihood)
    impact = int(impact)

    if not 1 <= likelihood <= 5:
        raise ValueError("Likelihood must be between 1 and 5.")

    if not 1 <= impact <= 5:
        raise ValueError("Impact must be between 1 and 5.")

    return likelihood * impact


def classify_risk(score):
    """Classify risk scores using this project's illustrative thresholds."""
    if score >= 20:
        return "Critical"
    elif score >= 12:
        return "High"
    elif score >= 6:
        return "Medium"
    else:
        return "Low"


def load_risks():
    """Read the risk register and calculate scores for every risk."""
    with RISK_FILE.open("r", newline="", encoding="utf-8") as file:
        risks = list(csv.DictReader(file))

    for risk in risks:
        score = calculate_risk_score(
            risk["likelihood"],
            risk["impact"],
        )
        risk["risk_score"] = score
        risk["risk_level"] = classify_risk(score)

    return risks


if __name__ == "__main__":
    for risk in load_risks():
        print(
            f'{risk["risk_id"]} | '
            f'{risk["risk_title"]} | '
            f'Score: {risk["risk_score"]} | '
            f'Level: {risk["risk_level"]}'
        )
