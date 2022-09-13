from src.services import user_service
from src.view_models.shared.viewmodel_base import ViewModelBase


class RegisterViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.name = self.request_dict.name
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()

    def validate(self):
        if not self.name:
            self.error = 'You must specify a name.'

        elif not self.email:
            self.error = 'Email field missing.'

        elif not self.password.strip():
            self.error = 'Password field missing.'

        elif len(self.password.strip()) < 6:
            self.error = 'Password must be at least 6 characters long.'

        elif user_service.find_user_by_email(self.email):
            self.error = 'A user with that email already exists.'
