from src.view_models.shared.viewmodel_base import ViewModelBase


class ActivationViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

    def validate(self):
        if not self.user:
            self.error = 'No user logged in.'
