""" all constants for the core_main_registry_app
"""


class DataStatus(object):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'


class DataRole(object):
    role = {'Organization': 'Organization',
            'DataCollection': 'Data Collection',
            'Dataset': 'Dataset',
            'ServiceAPI': 'Service',
            'WebSite': 'Informational Site',
            'Software': 'Software',
            'Database': 'Database'}
