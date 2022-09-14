from src.services.completion_service import get_completions_by_user_id
from src.view_models.shared.viewmodel_base import ViewModelBase


class HistoryViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.completions: list = get_completions_by_user_id(self.user_id)

    def validate(self) -> bool:
        """ Validate the prompt and remaining calls. """

        if self.error is not None:
            return False

        if self.completions is None:
            self.error = 'Error: Problem retrieving completions.'
            return False

        return True
