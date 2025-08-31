"""Debug field counting to understand the discrepancy."""


def test_analyze_field_structure():
    from tests.helpers.field_testing import create_marriage_field_tester

    analyze_field_structure()
    count_by_your_logic()


def analyze_field_structure():
    from tests.helpers.field_testing import create_marriage_field_tester

    tester = create_marriage_field_tester()
    all_fields = tester.get_all_fields()

    print(f"Total fields found: {len(all_fields)}")

    # Group fields by prefix (box type)
    by_prefix = {}
    for field in all_fields:
        field_id = field.get("id", "unknown")
        field_type = field.get("type", "unknown")

        # Get the first part before the first dot
        if "." in field_id:
            prefix = field_id.split(".")[0]
        else:
            prefix = "no_prefix"

        if prefix not in by_prefix:
            by_prefix[prefix] = {"total": 0, "by_type": {}}

        by_prefix[prefix]["total"] += 1
        if field_type not in by_prefix[prefix]["by_type"]:
            by_prefix[prefix]["by_type"][field_type] = 0
        by_prefix[prefix]["by_type"][field_type] += 1

    print(f"\n=== FIELDS BY PREFIX ===")
    total_manual = 0
    for prefix, data in sorted(by_prefix.items()):
        print(f"{prefix}: {data['total']} fields")
        total_manual += data["total"]
        for field_type, count in sorted(data["by_type"].items()):
            print(f"  {field_type}: {count}")

    print(f"\nManual total: {total_manual}")

    # Show some specific examples
    print(f"\n=== SAMPLE FIELD IDs ===")
    for i, field in enumerate(all_fields[:20]):  # First 20
        field_id = field.get("id", "unknown")
        field_type = field.get("type", "unknown")
        print(f"{i+1:2d}. {field_id} ({field_type})")

    if len(all_fields) > 20:
        print(f"... and {len(all_fields) - 20} more")


def count_by_your_logic():
    """Count according to user's logic to find the difference."""
    from tests.helpers.field_testing import create_marriage_field_tester

    tester = create_marriage_field_tester()
    all_fields = tester.get_all_fields()

    # User's expected counts
    common_expected = 6
    groom_expected = 23  # 11 + 12 landowner
    bride_expected = 25  # 13 + 12 landowner
    witness_pairs_expected = 84  # 4 pairs × (9 + 12)
    clergymen_expected = 16  # 2 × 8

    user_total = common_expected + groom_expected + bride_expected + witness_pairs_expected + clergymen_expected
    print(f"\nUser's expected total: {user_total}")
    print(f"Actual found: {len(all_fields)}")
    print(f"Difference: {len(all_fields) - user_total}")

    # Let's count by prefixes
    prefixes = {}
    for field in all_fields:
        field_id = field.get("id", "unknown")
        if "." in field_id:
            prefix = field_id.split(".")[0]
            prefixes[prefix] = prefixes.get(prefix, 0) + 1

    print(f"\n=== ACTUAL COUNTS BY PREFIX ===")
    for prefix, count in sorted(prefixes.items()):
        print(f"{prefix}: {count} fields")


if __name__ == "__main__":
    analyze_field_structure()
    count_by_your_logic()
