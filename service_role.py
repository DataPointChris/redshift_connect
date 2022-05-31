from helpers import create_user_password

DOMAIN = 'ichrisbirch.com'


class ServiceRole:
    def __init__(self, application, service_role, environment):
        self.application = application
        self.service_role = service_role
        self.environment = environment
        self.env_prefix = environment.get('env_prefix')
        self.service_account_suffix = environment.get('service_account_suffix')

        group = f'{self.env_prefix}-{self.application}-{self.service_role}'
        service_user = f's-{self.env_prefix}-{self.application}-{self.service_role}-{self.service_account_suffix}@{DOMAIN}'

        self.create_group_sql = f'create group "{group}";'
        password = create_user_password(12)
        self.create_service_user_sql = f'''create user "{service_user}" password '{password}';'''
        self.alter_default_privileges_service_account = f'alter default privileges for user "{service_user}" grant select on tables to group "{group}";'
        self.grant_usage_to_service_account_ing = (
            f'grant usage on schema "{self.application}_ing" to group "{group}"'
        )
        self.grant_create_to_service_account_ing = (
            f'grant create on schema "{self.application}_ing" to group "{group}"'
        )
        self.grant_all_on_tables_to_service_account_ing = (
            f'grant all on all tables in schema {self.application}_ing to group "{group}"'
        )

        self.grant_usage_to_service_account_trn = (
            f'grant usage on schema "{self.application}_trn" to group "{group}"'
        )
        self.grant_create_to_service_account_trn = (
            f'grant create on schema "{self.application}_trn" to group "{group}"'
        )
        self.grant_all_on_tables_to_service_account_trn = (
            f'grant all on all tables in schema {self.application}_trn to group "{group}"'
        )
