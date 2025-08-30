from forms.forms.marriage.dataclasses import FormStateTyped
from services.form_state_base import FormStateBase


class FormState(FormStateBase):
    def __init__(self) -> None:
        super().__init__()
        self.typed = FormStateTyped()
