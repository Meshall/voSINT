from vosint.models import Case


def print_summary(case: Case) -> None:
    print("\n=== voSINT Summary ===")
    print(f"Case: {case.case_id}")
    print(f"Mode: {case.mode}")
    print(f"Hits: {len(case.hits)}")
    if case.hits:
        print(f"Likely earliest source: {case.hits[0].url}")
    if case.failures:
        print("Provider failures:")
        for f in case.failures:
            print(f" - {f['provider']}: {f['error']}")
