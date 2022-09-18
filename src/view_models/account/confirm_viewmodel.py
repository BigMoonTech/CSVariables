from src.view_models.shared.viewmodel_base import ViewModelBase
from src.infrastructure.email_token import generate_token


class ConfirmViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()


    def validate(self):
        if not self.user_id:
            self.error = 'You must be logged in.'
