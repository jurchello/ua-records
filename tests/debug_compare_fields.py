"""Compare fields between bride subject_person and groom landowner."""


def test_compare_bride_vs_groom_landowner():
    from tests.helpers.field_testing import create_marriage_field_tester

    tester = create_marriage_field_tester()
    all_fields = tester.get_all_fields()

    # Extract specific field groups
    bride_subject_fields = []
    groom_landowner_fields = []

    for field in all_fields:
        field_id = field.get("id", "")
        field_type = field.get("type", "")

        if field_id.startswith("bride_box.subject_person."):
            bride_subject_fields.append(
                {"id": field_id, "type": field_type, "suffix": field_id.replace("bride_box.subject_person.", "")}
            )
        elif field_id.startswith("groom_box.landowner."):
            groom_landowner_fields.append(
                {"id": field_id, "type": field_type, "suffix": field_id.replace("groom_box.landowner.", "")}
            )

    print(f"BRIDE SUBJECT_PERSON: {len(bride_subject_fields)} fields")
    for field in sorted(bride_subject_fields, key=lambda x: x["suffix"]):
        print(f"  {field['suffix']} ({field['type']})")

    print(f"\nGROOM LANDOWNER: {len(groom_landowner_fields)} fields")
    for field in sorted(groom_landowner_fields, key=lambda x: x["suffix"]):
        print(f"  {field['suffix']} ({field['type']})")

    # Find differences
    bride_suffixes = {f["suffix"] for f in bride_subject_fields}
    groom_suffixes = {f["suffix"] for f in groom_landowner_fields}

    only_in_bride = bride_suffixes - groom_suffixes
    only_in_groom_landowner = groom_suffixes - bride_suffixes
    common = bride_suffixes & groom_suffixes

    print(f"\nCOMMON FIELDS: {len(common)}")
    for suffix in sorted(common):
        print(f"  {suffix}")

    print(f"\nONLY IN BRIDE SUBJECT_PERSON: {len(only_in_bride)}")
    for suffix in sorted(only_in_bride):
        print(f"  {suffix}")

    print(f"\nONLY IN GROOM LANDOWNER: {len(only_in_groom_landowner)}")
    for suffix in sorted(only_in_groom_landowner):
        print(f"  {suffix}")


def test_compare_all_person_types():
    """Compare all person type components to see differences."""
    from tests.helpers.field_testing import create_marriage_field_tester

    tester = create_marriage_field_tester()
    all_fields = tester.get_all_fields()

    # Group by component type
    components = {}

    for field in all_fields:
        field_id = field.get("id", "")
        field_type = field.get("type", "")

        # Parse to get component type
        parts = field_id.split(".")
        if len(parts) >= 3:
            box = parts[0]
            component = parts[1]
            sub_field = ".".join(parts[2:])

            comp_key = f"{box}.{component}"
            if comp_key not in components:
                components[comp_key] = []
            components[comp_key].append({"suffix": sub_field, "type": field_type, "full_id": field_id})

    print("=== ALL PERSON COMPONENTS COMPARISON ===")
    for comp_key in sorted(components.keys()):
        fields = components[comp_key]
        print(f"\n{comp_key}: {len(fields)} fields")
        for field in sorted(fields, key=lambda x: x["suffix"]):
            print(f"  {field['suffix']} ({field['type']})")


if __name__ == "__main__":
    test_compare_bride_vs_groom_landowner()
    print("\n" + "=" * 60)
    test_compare_all_person_types()
