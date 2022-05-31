service_roles = ['ingest', 'transform', 'tableau-egress', 'powerbi-egress']
app_names = ['core', 'google', 'facebook', 'airbnb', 'github', 'microsoft']

APPLICATIONS = {app_name: {'service_roles': service_roles} for app_name in app_names}


class Application:
    def __init__(self, application, environment):
        self.env_prefix = environment.get('env_prefix')
        self.application = application
        self.dev_role = environment.get('dev_role')
        self.service_roles = APPLICATIONS.get(self.application).get('service_roles')

        self.create_support_group_sql = (
            f'create group "{self.env_prefix}-{self.application}-{self.dev_role}";'
        )
