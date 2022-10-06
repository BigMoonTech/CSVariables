from src.services import user_service
from src.services.user_service import validate_password
from src.view_models.shared.viewmodel_base import ViewModelBase


class RegisterViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.name = self.request_dict.name.strip()
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()
        self.confirm_url = None

    def validate(self):
        if self.name == '':
            self.name = 'Emanon'  # Set a default name if none is provided

        if len(self.name) > 33:
            self.error = 'Name cannot be more than 32 characters long.'

        elif not self.email:
            self.error = 'Email field missing.'  # client-side validation should prevent this

        elif not self.password:
            self.error = 'Password field missing.'  # client-side validation should prevent this

        elif not validate_password(self.password):
            self.error = 'Check password requirements... At least 6 characters, one number, ' \
                         'one letter, only the special characters: !@.-_'

        elif user_service.find_user_by_email(self.email):
            self.error = 'A user with that email already exists.'
