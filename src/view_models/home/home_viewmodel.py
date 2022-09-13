import sqlite3

from src.services import user_service
from src.helpers import helper_functions as helpers
from src.view_models.shared.viewmodel_base import ViewModelBase


class HomeViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.total_requests = user_service.get_total_requests()

        # the value we will send to the textarea named output
        self.resp_text = ''

        # if the user is not logged in, set the user to get_unregistered_user_by_ip()
        if not self.user_id:
            self.ip_address = helpers.get_ip_address()
            self.user = user_service.get_unregistered_user_by_ip(self.ip_address)
            if self.user is None:
                self.user = user_service.create_unregistered_user(self.ip_address)
            self.remaining_calls = self.user.remaining_calls

        # if the user is logged in, get their remaining calls
        else:
            self.remaining_calls = self.user.remaining_monthly_calls



    def validate(self) -> bool:
        if self.remaining_calls <= 0:
            self.error = 'You have exceeded your free calls. Please register to continue using CSVE.'
            return False
        return True
