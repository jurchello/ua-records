from forms.forms.marriage.dataclasses import FormStateTyped
from services.form_state_base import FormStateBase


class FormState(FormStateBase):
    def __init__(self) -> None:
        super().__init__()
        self.typed = FormStateTyped()
    
    def _get_type_conversions(self) -> dict[str, type]:
        """Specify which fields need type conversion for marriage form"""
        return {
            "groom_box.subject_person.age": int,
            "bride_box.subject_person.age": int,
            "groom_box.subject_person.marriages_count": int,
            "bride_box.subject_person.marriages_count": int,
            "groom_box.subject_person.allow_empty": bool,
            "bride_box.subject_person.allow_empty": bool,
            "groom_box.landowner.allow_empty": bool,
            "bride_box.landowner.allow_empty": bool,
            "groom_box.witness_box_1.subject_person.allow_empty": bool,
            "groom_box.witness_box_1.landowner.allow_empty": bool,
            "groom_box.witness_box_2.subject_person.allow_empty": bool,
            "groom_box.witness_box_2.landowner.allow_empty": bool,
            "bride_box.witness_box_1.subject_person.allow_empty": bool,
            "bride_box.witness_box_1.landowner.allow_empty": bool,
            "bride_box.witness_box_2.subject_person.allow_empty": bool,
            "bride_box.witness_box_2.landowner.allow_empty": bool,
            "clergymen_box.clergyman_1.allow_empty": bool,
            "clergymen_box.clergyman_2.allow_empty": bool,
        }
