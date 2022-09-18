from src.services import user_service
from src.view_models.shared.viewmodel_base import ViewModelBase


class PwUpdateViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.current_password = self.request_dict.current_password
        self.new_password = self.request_dict.new_password
        self.confirm_password = self.request_dict.confirm_password

    def validate(self):
        """ Validate if the fields have been filled out correctly. """

        if not self.current_password:
            self.error = 'Password field required.'

        elif not self.new_password:
            self.error = 'New password field required.'

        elif not self.confirm_password:
            self.error = 'Confirm password field required.'

        elif self.new_password.strip() != self.new_password or len(self.new_password.split()) != 1:
            self.error = 'Passwords cannot contain spaces.'

        # verify the new passwords match
        elif self.new_password != self.confirm_password:
            self.error = 'Passwords do not match.'

        # verify the old password is correct
        elif not user_service.verify_hash(self.user.hashed_pw, self.current_password):
            self.error = 'Could not verify account. Please ensure the old password was entered correctly.'

        # verify the new password is different from the old password
        elif user_service.verify_hash(self.user.hashed_pw, self.new_password):
            self.error = 'New password cannot be the same as the old password.'


class EmailUpdateViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.new_email = self.request_dict.new_email
        self.confirm_email = self.request_dict.confirm_email

    def validate(self):
        """ Validate if the fields have been filled out correctly. """

        if not self.new_email:
            self.error = 'New email field required.'

        elif not self.confirm_email:
            self.error = 'Confirm email field required.'

        elif self.new_email.strip() != self.new_email or len(self.new_email.split()) != 1:
            self.error = 'No spaces allowed in email.'

        # verify the new passwords match
        elif self.new_email != self.confirm_email:
            self.error = 'Email fields do not match.'

        # verify the new email is different from the old email
        elif self.user.email == self.new_email:
            self.error = 'New email cannot be the same as the old email.'
