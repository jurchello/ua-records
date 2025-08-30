"""Helper utilities for comprehensive form field testing."""

from __future__ import annotations
from typing import Dict, List, Any, Set


class FormFieldTester:
    """Comprehensive testing utility for form fields."""
    
    def __init__(self, form_config: Dict[str, Any]):
        self.form_config = form_config
        self._all_fields = None
        self._field_types = None
    
    def get_all_fields(self) -> List[Dict[str, Any]]:
        """Extract all fields from form configuration."""
        if self._all_fields is not None:
            return self._all_fields
            
        fields = []
        for tab in self.form_config.get('tabs', []):
            for frame in tab.get('frames', []):
                for field in frame.get('fields', []):
                    if field.get('id') and field.get('type'):
                        fields.append(field)
        
        self._all_fields = fields
        return fields
    
    def get_unique_field_types(self) -> Set[str]:
        """Get all unique field types in the form."""
        if self._field_types is not None:
            return self._field_types
            
        types = set()
        for field in self.get_all_fields():
            field_type = field.get('type')
            if field_type:
                types.add(field_type)
        
        self._field_types = types
        return types
    
    def get_fields_by_type(self, field_type: str) -> List[Dict[str, Any]]:
        """Get all fields of specific type."""
        return [field for field in self.get_all_fields() 
                if field.get('type') == field_type]
    
    def get_testable_fields(self) -> List[Dict[str, Any]]:
        """Get fields that have model_path or id and can be tested with FormState."""
        testable = []
        for field in self.get_all_fields():
            # Try model_path first, fallback to id
            model_path = field.get('model_path') or field.get('id')
            field_type = field.get('type')
            
            # Must have path with dot notation
            if not isinstance(model_path, str) or '.' not in model_path:
                continue
                
            # Must be a testable field type
            if field_type in self.get_testable_field_types():
                testable.append(field)
        
        return testable
    
    def get_testable_field_types(self) -> Set[str]:
        """Get field types that can be tested with FormState."""
        return {
            'entry', 'text', 'textarea',  # Text fields
            'person', 'place', 'citation',  # Reference fields
            'date',  # Date fields
            'select', 'dropdown',  # Selection fields
            'checkbox', 'radio',  # Boolean/choice fields
        }
    
    def get_untestable_fields(self) -> List[Dict[str, Any]]:
        """Get fields that cannot be tested (no model_path/id or unsupported type)."""
        untestable = []
        testable_types = self.get_testable_field_types()
        
        for field in self.get_all_fields():
            # Try model_path first, fallback to id
            model_path = field.get('model_path') or field.get('id')
            field_type = field.get('type')
            
            # No path or not dot notation
            if not isinstance(model_path, str) or '.' not in model_path:
                untestable.append(field)
                continue
            
            # Unsupported field type
            if field_type not in testable_types:
                untestable.append(field)
                continue
        
        return untestable
    
    def generate_test_value(self, field_type: str, field_config: Dict[str, Any]) -> Any:
        """Generate appropriate test value for field type."""
        if field_type in ['entry', 'text', 'textarea']:
            return f"test_text_value_{field_config.get('id', 'unknown')}"
        
        elif field_type == 'person':
            return {
                "handle": f"test_handle_{field_config.get('id', 'unknown')}", 
                "gramps_id": f"I{hash(field_config.get('id', '')) % 9999:04d}"
            }
        
        elif field_type in ['place', 'citation']:
            return {
                "handle": f"test_{field_type}_handle_{field_config.get('id', 'unknown')}", 
                "gramps_id": f"{field_type.upper()[0]}{hash(field_config.get('id', '')) % 9999:04d}"
            }
        
        elif field_type == 'date':
            return "2024-01-01"  # Simple date string
        
        elif field_type in ['select', 'dropdown']:
            # Use first option if available, otherwise generic value
            options = field_config.get('options', [])
            if options and isinstance(options[0], dict):
                return options[0].get('value', 'test_option')
            return 'test_option'
        
        elif field_type == 'checkbox':
            return True
        
        elif field_type == 'radio':
            return field_config.get('default', 'test_radio_value')
        
        else:
            return f"test_value_{field_type}"
    
    def test_all_fields_with_form_state(self, form_state_class):
        """Test all testable fields with FormState."""
        results = {
            'success': [],
            'failed': [],
            'untestable': [],
            'field_type_coverage': {}
        }
        
        form_state = form_state_class()
        testable_fields = self.get_testable_fields()
        untestable_fields = self.get_untestable_fields()
        
        results['untestable'] = untestable_fields
        
        # Test each testable field
        for field in testable_fields:
            field_id = field.get('id')
            field_type = field.get('type')
            # Try model_path first, fallback to id
            model_path = field.get('model_path') or field.get('id')
            
            try:
                # Parse path
                parts = model_path.split('.', 1)
                prefix = parts[0]
                key = parts[1]
                
                # Generate and set test value
                test_value = self.generate_test_value(field_type, field)
                form_state.set(prefix, key, test_value, allow_log=False)
                
                # Verify the value was set
                retrieved_value = form_state.get(prefix, key)
                
                if self._values_match(test_value, retrieved_value, field_type):
                    results['success'].append({
                        'field_id': field_id,
                        'field_type': field_type,
                        'model_path': model_path,
                        'test_value': test_value,
                        'retrieved_value': retrieved_value
                    })
                else:
                    results['failed'].append({
                        'field_id': field_id,
                        'field_type': field_type,
                        'model_path': model_path,
                        'test_value': test_value,
                        'retrieved_value': retrieved_value,
                        'error': 'Values do not match'
                    })
                
            except Exception as e:
                results['failed'].append({
                    'field_id': field_id,
                    'field_type': field_type,
                    'model_path': model_path,
                    'error': str(e)
                })
            
            # Track field type coverage
            if field_type not in results['field_type_coverage']:
                results['field_type_coverage'][field_type] = {'total': 0, 'success': 0, 'failed': 0}
            results['field_type_coverage'][field_type]['total'] += 1
            
            # Check if this test was successful
            was_successful = any(r['field_id'] == field_id for r in results['success'])
            if was_successful:
                results['field_type_coverage'][field_type]['success'] += 1
            else:
                results['field_type_coverage'][field_type]['failed'] += 1
        
        return results
    
    def _values_match(self, expected: Any, actual: Any, field_type: str) -> bool:
        """Check if test value matches retrieved value."""
        if field_type in ['person', 'place', 'citation']:
            # For reference fields, compare as dictionaries
            if not isinstance(actual, dict) or not isinstance(expected, dict):
                return False
            return (actual.get('handle') == expected.get('handle') and 
                   actual.get('gramps_id') == expected.get('gramps_id'))
        else:
            # For simple fields, direct comparison
            return actual == expected
    
    def print_coverage_report(self, results: Dict[str, Any]) -> None:
        """Print a detailed coverage report."""
        total_fields = len(self.get_all_fields())
        testable_fields = len(self.get_testable_fields())
        untestable_fields = len(results['untestable'])
        successful_tests = len(results['success'])
        failed_tests = len(results['failed'])
        attempted_tests = successful_tests + failed_tests
        
        print(f"\n=== FORM FIELD TESTING COVERAGE REPORT ===")
        print(f"Total fields in form: {total_fields}")
        print(f"Testable fields: {testable_fields}")
        print(f"Untestable fields: {untestable_fields}")
        print(f"Fields actually tested: {attempted_tests}")
        print(f"Successful tests: {successful_tests}")
        print(f"Failed tests: {failed_tests}")
        print(f"Success rate: {successful_tests/testable_fields*100:.1f}%" if testable_fields > 0 else "N/A")
        print(f"Test execution rate: {attempted_tests/testable_fields*100:.1f}%" if testable_fields > 0 else "N/A")
        
        print(f"\n=== FIELD TYPE COVERAGE ===")
        total_by_type = 0
        for field_type, stats in results['field_type_coverage'].items():
            success_rate = stats['success']/stats['total']*100 if stats['total'] > 0 else 0
            total_by_type += stats['total']
            print(f"{field_type}: {stats['success']} success / {stats.get('failed', 0)} failed / {stats['total']} total ({success_rate:.1f}% success rate)")
        print(f"Total counted by types: {total_by_type}")
        
        if results['failed']:
            print(f"\n=== FAILED FIELDS ===")
            for failed in results['failed'][:5]:  # Show first 5 failures
                print(f"- {failed['field_id']} ({failed['field_type']}): {failed.get('error', 'Unknown error')}")
            if len(results['failed']) > 5:
                print(f"... and {len(results['failed']) - 5} more")
        
        if results['untestable']:
            print(f"\n=== UNTESTABLE FIELDS ===")
            for untestable in results['untestable'][:5]:  # Show first 5
                reason = "No model_path" if not untestable.get('model_path') else f"Unsupported type: {untestable.get('type')}"
                print(f"- {untestable['id']} ({untestable.get('type', 'unknown')}): {reason}")
            if len(results['untestable']) > 5:
                print(f"... and {len(results['untestable']) - 5} more")


def create_marriage_field_tester():
    """Create a FormFieldTester for the marriage form."""
    from forms.forms.marriage.config import FORM_EXPANDED
    marriage_config = FORM_EXPANDED['marriage']
    return FormFieldTester(marriage_config)