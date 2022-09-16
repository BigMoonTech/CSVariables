from src.services import user_service
from src.view_models.shared.viewmodel_base import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = user_service.find_user_by_id(self.user_id)

    def validate(self):
        """ Validate the user. """

        if not self.user:
            self.error = 'No user found with that ID.'
