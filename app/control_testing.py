import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def read_csv(filename):
    with (DATA_DIR / filename).open(
        "r", newline="", encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def analyse_tests():
    controls = read_csv("control_library.csv")
    tests = read_csv("control_tests.csv")

    control_ids = {control["control_id"] for control in controls}
    errors = []

    for test in tests:
        if test["control_id"] not in control_ids:
            errors.append(
                f'{test["test_id"]}: unknown control '
                f'{test["control_id"]}'
            )
            continue

        try:
            sample_size = int(test["sample_size"])
            exceptions = int(test["exceptions_found"])
        except ValueError:
            errors.append(f'{test["test_id"]}: invalid numeric values')
            continue

        if sample_size <= 0:
            errors.append(f'{test["test_id"]}: sample size must be positive')
            continue

        if exceptions < 0 or exceptions > sample_size:
            errors.append(
                f'{test["test_id"]}: exceptions must be between '
                'zero and sample size'
            )
            continue

        test["exception_rate"] = round(
            exceptions / sample_size * 100, 2
        )

    return tests, errors


def main():
    tests, errors = analyse_tests()

    print("CONTROL TESTING SUMMARY")
    print("=" * 60)

    for test in tests:
        rate = test.get("exception_rate")
        if rate is None:
            print(f'{test["test_id"]}: INVALID DATA')
            continue

        print(
            f'{test["test_id"]} | {test["control_id"]} | '
            f'Result: {test["result"]} | '
            f'Exceptions: {test["exceptions_found"]}/'
            f'{test["sample_size"]} | Rate: {rate}%'
        )

    print(f"\nTests processed: {len(tests)}")
    print(f"Validation errors: {len(errors)}")

    for error in errors:
        print(f"- {error}")


if __name__ == "__main__":
    main()
