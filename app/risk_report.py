from collections import Counter
from risk_engine import load_risks


def main():
    risks = load_risks()
    counts = Counter(risk["risk_level"] for risk in risks)

    print("\nENTERPRISE GRC — RISK SUMMARY")
    print("=" * 38)
    print(f"Total risks: {len(risks)}")

    for level in ["Critical", "High", "Medium", "Low"]:
        print(f"{level:10}: {counts.get(level, 0)}")

    print("\nRisks requiring attention:")
    for risk in risks:
        if risk["risk_level"] in ["Critical", "High"]:
            print(
                f'- {risk["risk_id"]}: {risk["risk_title"]} '
                f'(score {risk["risk_score"]})'
            )


if __name__ == "__main__":
    main()
