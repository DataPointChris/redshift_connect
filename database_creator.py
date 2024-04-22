# %% [markdown]
# # Database Creator

# %% [markdown]
# Need to make/finish the functions to make the domain and subdomain lists

# %%
from security_domains import SECURITY_DOMAINS
from environments import ENVIRONMENTS

# %%
dev = ENVIRONMENTS.get('dev')
test = ENVIRONMENTS.get('test')
prod = ENVIRONMENTS.get('prod')

# %%
# WIP
def make_security_groups_from_domain_subdomain(domain, subdomain):
    pass


def add_domain(env=None, info=None, template=False):
    """Use template=True to output an example dictionary"""
    pass


def add_subdomain(env=None, domain=None, subdomains=None, template=False):
    """Use template=True to output an example dictionary"""
    sensitive = info.get('sensitive')
    for subdomain in subdomains:
        for sg in subdomain.get('security_groups'):
            add_security_group(
                env=env, domain=domain, subdomain=subdomain, sensitive=sensitive
            )
    pass

# %%
# ADD_SECURITY_GROUP IS WORKING
def add_security_group(env, domain, subdomain=None, sensitive=None):
    env_prefix = env.get('env_prefix')
    sensitive_suffix = env.get('sensitive_suffix')
    group_parts = [env_prefix, domain]
    if subdomain is not None:
        group_parts.append(subdomain)
    if sensitive is not None:
        if sensitive == 'replace':
            # add senstivie_suffix to end
            group_parts.append(sensitive_suffix)
        elif sensitive == 'add_extra':
            # add extra security group with sensitive_suffix
            group_parts_sen = group_parts.copy()
            group_parts_sen.append(sensitive_suffix)
            security_group_sen = '-'.join(group_parts_sen)
            add_group_sen_sql = f'''add group "{security_group_sen}";'''
        else:
            raise ValueError(
                f'sensitive must be either `add_extra` or `replace`, got `{sensitive}`'
            )
    security_group = '-'.join(group_parts)
    add_group_sql = f'''add group "{security_group}";'''
    if sensitive == 'add_extra':
        return [add_group_sql, add_group_sen_sql]
    else:
        return [add_group_sql]


# %%
add_security_group(
    env=dev, domain='widget', subdomain='master', sensitive='add_extra'
)


# %%
add_security_group(
    env=ENVIRONMENTS.get('prod'), domain='api', subdomain='master', sensitive='replace'
)

# %%
# PRINT_DATABASE_DOMAINS IS WORKING
def print_database_domains(database, indent_chars=10):
    """prints the database domains, subdomains, and security groups"""

    def print_indent(item, level, type):
        indent_string = ' ' * level * indent_chars
        sep = '-'
        if type == 'security_domain':
            print_string = item.upper() + ' -- Security Domain'
            print(print_string)
            print(sep * len(print_string))
        elif type == 'domain':
            print_string = indent_string + item.upper() + ' -- Data Domain'
            print(print_string)
            print(
                ' ' * len(indent_string) + sep * (len(print_string) - len(indent_string))
            )
        elif type == 'subdomain':
            print_string = indent_string + item.upper() + ' -- Subdomain'
            print(print_string)
            print(
                ' ' * len(indent_string) + sep * (len(print_string) - len(indent_string))
            )
        elif type == 'security_group':
            print(indent_string + item)

    def display_and_interpret_domain(domains, level, type):
        for name, domain in domains.items():
            print()
            print_indent(name, level, type=type)
            interpret(domain, level)

    def interpret(thing, level=-1):
        security_domains = thing.get('security_domains')
        domains = thing.get('domains')
        subdomains = thing.get('subdomains')
        security_groups = thing.get('security_groups')
        if security_groups is not None:
            for security_group in security_groups:
                print_indent(f"'{security_group}'", level, type='security_group')
        if subdomains is not None:
            level += 1
            display_and_interpret_domain(
                domains=subdomains, level=level, type='subdomain'
            )
        if domains is not None:
            level += 1
            display_and_interpret_domain(
                domains=domains, level=level, type='domain'
            )
        if security_domains is not None:
            level += 1
            display_and_interpret_domain(
                domains=security_domains, level=level, type='security_domain'
            )

    return interpret(database)


# %%
print_database_domains(SECURITY_DOMAINS, indent_chars=8)

# %%
# GET_DOMAIN_SECURITY_GROUPS IS WORKING
def get_domain_security_groups(database):
    """Get a list of data domain security groups"""
    security_group_list = []
    def reinterpret(domains):
        for name, domain in domains.items():
            interpret(domain)

    def interpret(thing):
        security_domains = thing.get('security_domains')
        domains = thing.get('domains')
        subdomains = thing.get('subdomains')
        security_groups = thing.get('security_groups')
        if security_groups is not None:
            for security_group in security_groups:
                if security_group != '':
                    security_group_list.append(security_group)
        if subdomains is not None:
            reinterpret(subdomains)
        if domains is not None:
            reinterpret(domains)
        if security_domains is not None:
            reinterpret(security_domains)
    
    interpret(database)
    return security_group_list


# %%
widgets_domain = SECURITY_DOMAINS['security_domains']['product']['domains']['widget']
for sg in get_domain_security_groups(widgets_domain):
    print(sg)

# %%



