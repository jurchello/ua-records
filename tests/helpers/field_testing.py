"""Helper utilities for comprehensive form field testing — id-only version."""

from __future__ import annotations
from typing import Dict, List, Any, Set


class FormFieldTester:
    """Comprehensive testing utility for form fields (id-based)."""

    def __init__(self, form_config: Dict[str, Any]):
        self.form_config = form_config
        self._all_fields: List[Dict[str, Any]] | None = None
        self._field_types: Set[str] | None = None

    def get_all_fields(self) -> List[Dict[str, Any]]:
        """Extract all fields from form configuration."""
        if self._all_fields is not None:
            return self._all_fields

        fields: List[Dict[str, Any]] = []
        for tab in self.form_config.get("tabs", []):
            for frame in tab.get("frames", []):
                for field in frame.get("fields", []):
                    if field.get("id") and field.get("type"):
                        fields.append(field)

        self._all_fields = fields
        return fields

    def get_unique_field_types(self) -> Set[str]:
        """Get all unique field types in the form."""
        if self._field_types is not None:
            return self._field_types

        types: Set[str] = set()
        for field in self.get_all_fields():
            t = field.get("type")
            if t:
                types.add(t)

        self._field_types = types
        return types

    def get_fields_by_type(self, field_type: str) -> List[Dict[str, Any]]:
        """Get all fields of specific type."""
        return [f for f in self.get_all_fields() if f.get("type") == field_type]

    def get_testable_fields(self) -> List[Dict[str, Any]]:
        """
        Fields are testable iff:
          - id is a dotted path "<prefix>.<rest>"
          - type is in supported set
        """
        testable: List[Dict[str, Any]] = []
        supported = self.get_testable_field_types()
        for f in self.get_all_fields():
            fid = f.get("id")
            t = f.get("type")
            if not isinstance(fid, str) or "." not in fid:
                continue
            if t in supported:
                testable.append(f)
        return testable

    def get_testable_field_types(self) -> Set[str]:
        """Field types that can be set on FormState in tests."""
        return {
            # text-ish
            "entry",
            "text",
            "textarea",
            "select",
            "dropdown",
            "date",
            # boolean
            "checkbox",
            "radio",
            # dnd/link-ish
            "person",
            "place",
            "citation",
        }

    def get_untestable_fields(self) -> List[Dict[str, Any]]:
        """Fields that cannot be tested (no dotted id or unsupported type)."""
        un: List[Dict[str, Any]] = []
        supported = self.get_testable_field_types()
        for f in self.get_all_fields():
            fid = f.get("id")
            t = f.get("type")
            if not isinstance(fid, str) or "." not in fid:
                un.append(f)
                continue
            if t not in supported:
                un.append(f)
        return un

    def generate_test_value(self, field_type: str, field_config: Dict[str, Any]) -> Any:
        """Generate appropriate test value for field type."""
        if field_type in {"entry", "text", "textarea"}:
            return f"test_text_value_{field_config.get('id', 'unknown')}"

        if field_type == "date":
            return "2024-01-01"

        if field_type in {"select", "dropdown"}:
            opts = field_config.get("options", [])
            if isinstance(opts, list) and opts:
                first = opts[0]
                if isinstance(first, dict):
                    return first.get("value") or first.get("id") or "test_option"
                if isinstance(first, str):
                    return first
            return "test_option"

        if field_type == "checkbox":
            return True

        if field_type == "radio":
            return field_config.get("default", "test_radio_value")

        if field_type in {"person", "place", "citation"}:
            # lightweight wrapper: FormState не вимагає object для встановлення
            prefix = field_type.upper()[0]
            return {
                "handle": f"test_{field_type}_handle_{field_config.get('id', 'unknown')}",
                "gramps_id": f"{prefix}{abs(hash(field_config.get('id',''))) % 9999:04d}",
            }

        return f"test_value_{field_type}"

    def test_all_fields_with_form_state(self, form_state_class):
        """Test all testable fields with FormState (id-only)."""
        results = {
            "success": [],
            "failed": [],
            "untestable": [],
            "field_type_coverage": {},
        }

        form_state = form_state_class()
        testable = self.get_testable_fields()
        results["untestable"] = self.get_untestable_fields()

        for f in testable:
            fid = f.get("id")
            ftype = f.get("type")

            try:
                prefix, key = fid.split(".", 1)

                test_value = self.generate_test_value(ftype, f)
                form_state.set(prefix, key, test_value, allow_log=False)

                got = form_state.get(prefix, key)
                if self._values_match(test_value, got, ftype):
                    results["success"].append(
                        {
                            "field_id": fid,
                            "field_type": ftype,
                            "path": fid,
                            "test_value": test_value,
                            "retrieved_value": got,
                        }
                    )
                else:
                    results["failed"].append(
                        {
                            "field_id": fid,
                            "field_type": ftype,
                            "path": fid,
                            "test_value": test_value,
                            "retrieved_value": got,
                            "error": "Values do not match",
                        }
                    )
            except Exception as e:
                results["failed"].append({"field_id": fid, "field_type": ftype, "path": fid, "error": str(e)})

            cov = results["field_type_coverage"].setdefault(ftype, {"total": 0, "success": 0, "failed": 0})
            cov["total"] += 1
            if any(r["field_id"] == fid for r in results["success"]):
                cov["success"] += 1
            else:
                cov["failed"] += 1

        return results

    def _values_match(self, expected: Any, actual: Any, field_type: str) -> bool:
        """Check if test value matches retrieved value."""
        if field_type in {"person", "place", "citation"}:
            return (
                isinstance(actual, dict)
                and isinstance(expected, dict)
                and actual.get("handle") == expected.get("handle")
                and actual.get("gramps_id") == expected.get("gramps_id")
            )
        return actual == expected

    def print_coverage_report(self, results: Dict[str, Any]) -> None:
        """Print a detailed coverage report."""
        total_fields = len(self.get_all_fields())
        testable_fields = len(self.get_testable_fields())
        untestable_fields = len(results["untestable"])
        successful = len(results["success"])
        failed = len(results["failed"])
        attempted = successful + failed

        print("\n=== FORM FIELD TESTING COVERAGE REPORT ===")
        print(f"Total fields in form: {total_fields}")
        print(f"Testable fields: {testable_fields}")
        print(f"Untestable fields: {untestable_fields}")
        print(f"Fields actually tested: {attempted}")
        print(f"Successful tests: {successful}")
        print(f"Failed tests: {failed}")
        print(f"Success rate: {successful/testable_fields*100:.1f}%" if testable_fields > 0 else "Success rate: N/A")
        print(
            f"Test execution rate: {attempted/testable_fields*100:.1f}%"
            if testable_fields > 0
            else "Test execution rate: N/A"
        )

        print("\n=== FIELD TYPE COVERAGE ===")
        total_by_type = 0
        for ftype, stats in results["field_type_coverage"].items():
            total_by_type += stats["total"]
            sr = stats["success"] / stats["total"] * 100 if stats["total"] else 0.0
            print(
                f"{ftype}: {stats['success']} success / {stats.get('failed', 0)} failed / "
                f"{stats['total']} total ({sr:.1f}% success rate)"
            )
        print(f"Total counted by types: {total_by_type}")

        if results["failed"]:
            print("\n=== FAILED FIELDS ===")
            for failed in results["failed"][:5]:
                print(f"- {failed['field_id']} ({failed['field_type']}): " f"{failed.get('error', 'Unknown error')}")
            if len(results["failed"]) > 5:
                print(f"... and {len(results['failed']) - 5} more")

        if results["untestable"]:
            print("\n=== UNTESTABLE FIELDS ===")
            for u in results["untestable"][:5]:
                fid = u.get("id", "unknown")
                t = u.get("type", "unknown")
                reason = "id must contain a dot (prefix.key)"
                print(f"- {fid} ({t}): {reason}")
            if len(results["untestable"]) > 5:
                print(f"... and {len(results['untestable']) - 5} more")


def create_marriage_field_tester():
    """Create a FormFieldTester for the marriage form."""
    from forms.forms.marriage.config import FORM_EXPANDED

    marriage_config = FORM_EXPANDED["marriage"]
    return FormFieldTester(marriage_config)
