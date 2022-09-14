from src.services.completion_service import (
    valid_prompt_len, has_no_profanity, get_completions_by_uuid, create_empty_completion
)
from src.view_models.shared.viewmodel_base import ViewModelBase


class AppViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        # the value we will send to the textarea named output
        self.resp_text: str = ''

        if self.user_id is not None and self.user is not None:
            self.remaining_calls: int = self.user.remaining_monthly_calls
        else:
            self.error = 'Error: Problem retrieving user data.'
            self.remaining_calls: int = 0

        self.prompt = ""

    def validate(self) -> bool:
        """ Validate the prompt and remaining calls. """

        if self.error is not None:
            return False

        if self.remaining_calls <= 0:
            self.error = 'You have exceeded your monthly calls.'
            return False

        if self.prompt is None or self.prompt == '':
            self.error = 'Please enter a valid prompt.'
            return False

        if not valid_prompt_len(self.prompt):
            self.error = 'Cannot exceed 200 characters.'
            return False

        if not has_no_profanity(self.prompt):
            self.error = 'Cannot contain profanity.'
            return False

        return True
