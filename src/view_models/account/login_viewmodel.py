from src.view_models.shared.viewmodel_base import ViewModelBase


class LoginViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()

    def validate(self):
        if not self.email:
            self.error = 'Email field missing.'

        elif not self.password.strip():
            self.error = 'Password field missing.'
