APPLICATIONS = {
    'core': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'c360': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'ccpa': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'ecsc': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'emdm': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'fdw': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'irm': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'leo': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'ndw': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'nsh': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'pasa': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'p360': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'peff': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'q360': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
    'vdw': {
        'service_roles': ['integrate', 'tableau-egress', 'powerbi-egress'],
    },
}


class Application:
    def __init__(self, application, environment):
        self.env_prefix = environment.get('env_prefix')
        self.application = application
        self.dev_role = environment.get('dev_role')
        self.service_roles = APPLICATIONS.get(self.application).get('service_roles')

        self.create_support_group_sql = (
            f'create group "{self.env_prefix}-{self.application}-{self.dev_role}";'
        )
