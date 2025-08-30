"""Detailed analysis of each person's fields in marriage form."""

def test_detailed_field_analysis():
    from tests.helpers.field_testing import create_marriage_field_tester
    
    tester = create_marriage_field_tester()
    all_fields = tester.get_all_fields()
    
    print(f"Total fields: {len(all_fields)}\n")
    
    # Group by detailed path
    groups = {}
    for field in all_fields:
        field_id = field.get('id', '')
        field_type = field.get('type', '')
        
        # Parse the field path more carefully
        parts = field_id.split('.')
        if len(parts) >= 2:
            box = parts[0]  # groom_box, bride_box, etc
            person_or_component = parts[1]  # subject_person, landowner, witness_box_1, etc
            
            key = f"{box}.{person_or_component}"
            if key not in groups:
                groups[key] = {'fields': [], 'count': 0}
            groups[key]['fields'].append({'id': field_id, 'type': field_type})
            groups[key]['count'] += 1
        else:
            # Handle fields without proper structure
            key = f"OTHER.{field_id}"
            if key not in groups:
                groups[key] = {'fields': [], 'count': 0}
            groups[key]['fields'].append({'id': field_id, 'type': field_type})
            groups[key]['count'] += 1
    
    # Print analysis
    print("=== DETAILED FIELD COUNTS BY PERSON/COMPONENT ===")
    total_manual = 0
    
    # Sort groups for better readability
    for group_key in sorted(groups.keys()):
        group_data = groups[group_key]
        count = group_data['count']
        total_manual += count
        
        print(f"\n{group_key}: {count} fields")
        
        # Show field types breakdown
        type_counts = {}
        for field in group_data['fields']:
            ftype = field['type']
            type_counts[ftype] = type_counts.get(ftype, 0) + 1
        
        for ftype, type_count in sorted(type_counts.items()):
            print(f"  {ftype}: {type_count}")
        
        # Show first few field IDs as examples
        if count <= 5:
            for field in group_data['fields']:
                print(f"    - {field['id']}")
        else:
            for field in group_data['fields'][:3]:
                print(f"    - {field['id']}")
            print(f"    - ... and {count - 3} more")
    
    print(f"\nManual total: {total_manual}")
    
    # Count persons specifically
    print("\n=== PERSON FIELD ANALYSIS ===")
    person_groups = [key for key in groups.keys() if any(field['type'] == 'person' for field in groups[key]['fields'])]
    
    for person_key in sorted(person_groups):
        person_fields = [f for f in groups[person_key]['fields'] if f['type'] == 'person']
        other_fields = [f for f in groups[person_key]['fields'] if f['type'] != 'person']
        print(f"{person_key}: {len(person_fields)} person fields, {len(other_fields)} other fields, {groups[person_key]['count']} total")
    
    print(f"\nTotal person components: {len(person_groups)}")
    
    # Your calculation check
    print("\n=== CALCULATION CHECK ===")
    print("Expected by user logic:")
    print("- Common: 6 fields")
    print("- Persons: 14 people × 13 fields each = 182 fields")  
    print("- Total expected: 188 fields")
    print(f"- Actual found: {len(all_fields)} fields")
    print(f"- Difference: {len(all_fields) - 188}")


if __name__ == "__main__":
    test_detailed_field_analysis()