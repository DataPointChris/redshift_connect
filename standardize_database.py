# %% [markdown]
# # Standardizing a Database

# %% [markdown]
# prefixes for all of the support groups  
# what ing or trn do they have access to?  
# What service-account(s) do they have?  
# what access does the service account have?

# %% [markdown]
# 

# %% [markdown]
# Making it work for all of the environ:
# 
# 

# %%
from environments import ENVIRONMENTS
from applications import APPLICATIONS, Application
from service_role import ServiceRole

# %%
DEFAULT_SCHEMAS = ['_ing', '_trn']


# %% [markdown]
# ## Applications
# 

# %%
# I think that the application isn't correct 
# by giving create permissions to the egress accounts.
# Also it should take in a parameter `schema_access` 
# and create the access patterns from that instead of hardcode trn and ing.  
# I think maybe this goes in `APPLICATIONS`

# %%
sql = {}

# ENVIRONMENTS
# Every env has applications
for env in ENVIRONMENTS:
    sql[env] = []
    environment = ENVIRONMENTS.get(env)
    
    # APPLICATIONS
    # Every application has service roles, prefix, group_name, support group
    for application in APPLICATIONS:
        app = Application(application, environment=environment)

        # SUPPORT GROUPS
        support_group_sql = app.create_support_group_sql
        sql[env].append(support_group_sql)
      
        # SERVICE ROLES
        # # Every service_role has env prefix, group name, service_role_name
        for service_role in app.service_roles:
            role = ServiceRole(application=app.application, service_role=service_role, environment=environment)
            service_account_sql = [
                role.create_group_sql,
                role.create_service_user_sql,
                role.alter_default_privileges_service_account,
                role.grant_usage_to_service_account_ing,
                role.grant_create_to_service_account_ing,
                role.grant_usage_to_service_account_trn,
                role.grant_create_to_service_account_trn,
            ]
            sql[env].extend(service_account_sql)
        # All of these hard-coded names are ugly and horrible
        # They should be functions instead of just attributes
        # Or have better names


# %%
sql['prod']

# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%



