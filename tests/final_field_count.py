"""Final detailed field count analysis to show exactly how we get 172 fields."""

def test_final_field_breakdown():
    from tests.helpers.field_testing import create_marriage_field_tester
    
    tester = create_marriage_field_tester()
    all_fields = tester.get_all_fields()
    
    print("=== ЗВЕДЕНІ ДАНІ: ЯК ВИХОДИТЬ 172 ПОЛЯ ===\n")
    
    # Group by main sections
    sections = {
        'common_box': [],
        'groom_box': [],
        'bride_box': [],
        'clergymen_box': []
    }
    
    for field in all_fields:
        field_id = field.get('id', '')
        field_type = field.get('type', '')
        
        for section_name in sections.keys():
            if field_id.startswith(section_name + '.'):
                sections[section_name].append({
                    'id': field_id,
                    'type': field_type
                })
                break
    
    total_check = 0
    
    # Common box analysis
    common_count = len(sections['common_box'])
    total_check += common_count
    print(f"1. COMMON_BOX: {common_count} полів")
    for field in sections['common_box']:
        suffix = field['id'].replace('common_box.', '')
        print(f"   - {suffix} ({field['type']})")
    
    # Detailed analysis for person boxes
    print(f"\n2. GROOM_BOX: {len(sections['groom_box'])} полів")
    groom_analysis = analyze_person_box(sections['groom_box'], 'groom_box')
    total_check += len(sections['groom_box'])
    print_person_box_analysis(groom_analysis)
    
    print(f"\n3. BRIDE_BOX: {len(sections['bride_box'])} полів")
    bride_analysis = analyze_person_box(sections['bride_box'], 'bride_box')
    total_check += len(sections['bride_box'])
    print_person_box_analysis(bride_analysis)
    
    print(f"\n4. CLERGYMEN_BOX: {len(sections['clergymen_box'])} полів")
    clergy_analysis = analyze_clergy_box(sections['clergymen_box'])
    total_check += len(sections['clergymen_box'])
    print_clergy_analysis(clergy_analysis)
    
    print(f"\n=== ПІДСУМОК ===")
    print(f"Common: {common_count}")
    print(f"Groom: {len(sections['groom_box'])}")
    print(f"Bride: {len(sections['bride_box'])}")
    print(f"Clergy: {len(sections['clergymen_box'])}")
    print(f"ВСЬОГО: {total_check}")
    
    print(f"\n=== РОЗБИВКА ЗА ОСОБАМИ ===")
    print(f"1. Common fields: 6")
    print(f"2. Groom subject_person: {count_fields_in_component(sections['groom_box'], 'subject_person')}")
    print(f"3. Groom landowner: {count_fields_in_component(sections['groom_box'], 'landowner')}")  
    print(f"4. Bride subject_person: {count_fields_in_component(sections['bride_box'], 'subject_person')}")
    print(f"5. Bride landowner: {count_fields_in_component(sections['bride_box'], 'landowner')}")
    print(f"6. Groom witness_box_1: {count_fields_in_component(sections['groom_box'], 'witness_box_1')}")
    print(f"7. Groom witness_box_2: {count_fields_in_component(sections['groom_box'], 'witness_box_2')}")
    print(f"8. Bride witness_box_1: {count_fields_in_component(sections['bride_box'], 'witness_box_1')}")
    print(f"9. Bride witness_box_2: {count_fields_in_component(sections['bride_box'], 'witness_box_2')}")
    print(f"10. Clergyman_1: {count_fields_in_component(sections['clergymen_box'], 'clergyman_1')}")
    print(f"11. Clergyman_2: {count_fields_in_component(sections['clergymen_box'], 'clergyman_2')}")
    
    manual_total = (6 + 
                   count_fields_in_component(sections['groom_box'], 'subject_person') +
                   count_fields_in_component(sections['groom_box'], 'landowner') +
                   count_fields_in_component(sections['bride_box'], 'subject_person') +
                   count_fields_in_component(sections['bride_box'], 'landowner') +
                   count_fields_in_component(sections['groom_box'], 'witness_box_1') +
                   count_fields_in_component(sections['groom_box'], 'witness_box_2') +
                   count_fields_in_component(sections['bride_box'], 'witness_box_1') +
                   count_fields_in_component(sections['bride_box'], 'witness_box_2') +
                   count_fields_in_component(sections['clergymen_box'], 'clergyman_1') +
                   count_fields_in_component(sections['clergymen_box'], 'clergyman_2'))
    
    print(f"\nПеревірка підрахунку особами: {manual_total}")


def count_fields_in_component(box_fields, component_name):
    """Count fields in specific component."""
    count = 0
    
    for field in box_fields:
        field_id = field['id']
        # Extract component from field id - it's the second part after box name
        parts = field_id.split('.')
        if len(parts) >= 3 and parts[1] == component_name:
            count += 1
    
    return count


def analyze_person_box(fields, box_name):
    """Analyze person box structure."""
    components = {}
    
    for field in fields:
        field_id = field['id']
        field_type = field['type']
        
        # Extract component name
        parts = field_id.replace(box_name + '.', '').split('.')
        component = parts[0]
        
        if component not in components:
            components[component] = []
        
        components[component].append({
            'id': field_id,
            'type': field_type,
            'suffix': '.'.join(parts[1:]) if len(parts) > 1 else ''
        })
    
    return components


def print_person_box_analysis(components):
    """Print person box analysis."""
    for comp_name, fields in sorted(components.items()):
        print(f"   {comp_name}: {len(fields)} полів")
        type_counts = {}
        for field in fields:
            ftype = field['type']
            type_counts[ftype] = type_counts.get(ftype, 0) + 1
        
        for ftype, count in sorted(type_counts.items()):
            print(f"     {ftype}: {count}")


def analyze_clergy_box(fields):
    """Analyze clergy box."""
    components = {}
    
    for field in fields:
        field_id = field['id']
        field_type = field['type']
        
        # Extract clergyman number
        parts = field_id.replace('clergymen_box.', '').split('.')
        component = parts[0]  # clergyman_1 or clergyman_2
        
        if component not in components:
            components[component] = []
        
        components[component].append({
            'id': field_id,
            'type': field_type
        })
    
    return components


def print_clergy_analysis(components):
    """Print clergy analysis."""
    for comp_name, fields in sorted(components.items()):
        print(f"   {comp_name}: {len(fields)} полів")
        type_counts = {}
        for field in fields:
            ftype = field['type']
            type_counts[ftype] = type_counts.get(ftype, 0) + 1
        
        for ftype, count in sorted(type_counts.items()):
            print(f"     {ftype}: {count}")


if __name__ == "__main__":
    test_final_field_breakdown()