from core_main_app.views.common.views import ViewData


class RegistryViewData(ViewData):
    def __init__(self):
        super(ViewData, self).__init__()
        self.template = 'core_main_registry_app/user/data/detail.html'
