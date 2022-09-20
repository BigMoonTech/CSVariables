from src.view_models.shared.viewmodel_base import ViewModelBase


class PasswordResetRequestViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.email = self.request_dict.email.lower().strip()
        self.confirm_url = None

    def validate(self):
        if not self.email:
            self.error = 'You must specify an email address.'


class PasswordResetFormViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.token = None
        self.password = self.request_dict.new_password
        self.confirm_password = self.request_dict.confirm_password

    def validate(self):
        if not self.password:
            self.error = 'You must specify a password.'

        elif not self.confirm_password:
            self.error = 'You must confirm your password.'

        elif self.password != self.confirm_password:
            self.error = 'The passwords do not match.'

        elif self.password.strip() != self.password or len(self.password.split()) != 1:
            self.error = 'Passwords cannot contain spaces.'

    def validate_token(self):
        if not self.token:
            self.error = 'There was a problem finding the authorized user. Probably because the password reset link ' \
                         'is invalid or expired.'
