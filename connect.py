# %%
from faker import Faker
from redshift_connection import RedshiftConnection
from tqdm.notebook import tqdm

# %%

conn = RedshiftConnection().connect()
c = conn.cursor()

fake = Faker()

def df(sql):
    return c.execute(sql).fetch_dataframe()

# %%
# conn.rollback()

# %% [markdown]
# ## Create

# %%
SCHEMAS = [
    'schema_parts',
    'schema_iron',
    'schema_sales',
    'schema_research',
    'schema_consumer',
    'schema_production',
]
GROUPS = [
    'group_marketing',
    'group_sales',
    'group_hr',
    'group_development',
    'group_engineering',
]
TABLES = [
    'table_a',
    'table_b',
    'table_c',
    'table_d',
    'table_e',
    'table_f',
    'table_h',
    'table_i',
    'table_j',
]

SCHEMA_GROUP_PERMISSIONS = {
    'schema_parts': ['group_development', 'group_engineering'],
    'schema_iron': ['group_engineering'],
    'schema_sales': ['group_sales', 'group_marketing'],
    'schema_research': ['group_development', 'group_engineering'],
    'schema_consumer': ['group_marketing', 'group_sales', 'group_hr', 'group_development'],
    'schema_production': ['group_engineering'],
}


# %%
DATABASE = {}
DATABASE['schemas'] = {}
DATABASE['groups'] = {}
schemas = DATABASE.get('schemas')
groups = DATABASE.get('groups')

for schema in SCHEMAS:
    schemas[schema] = {'tables': TABLES}

for group in GROUPS:
    groups[group] = {
        'users': [],
        'permissions': []
    }



DATABASE

# %%
test_schemas = [
    'marketing',
    'sales',
    'engineering',
    'manufacturing',
    'electrical',
    'hr',
    'batteries',
]

test_tables = [
    'table_a',
    'table_b',
    'table_c',
    'table_d',
    'table_e',
    'table_gg',
    'table_h',
    'table_i',
    'table_j',
]

test_tables = [f'{s}.{t}' for t in test_tables for s in test_schemas]


# %%
# c.execute('create schema if not exists admin;')
# conn.commit()

# %%
def df(sql):
    return c.execute(sql).fetch_dataframe()


def create_schema(name):
    c.execute(f"CREATE SCHEMA if not exists {name};")


def create_group(name):
    c.execute(f"CREATE GROUP {name};")


def grant_usage_and_select(schema, group):
    c.execute(f"GRANT USAGE on SCHEMA {schema} to GROUP {group};")
    c.execute(f"GRANT SELECT ON ALL TABLES IN SCHEMA {schema} TO GROUP {group};")


def create_table(table):
    c.execute(f'create table if not exists {table} (colors varchar(20))')


def _make_tuple_colors(num):
    return tuple(zip([fake.color_name() for _ in range(num)]))


def insert_colors_in_table(table):
    c.executemany(f'insert into {table} (colors) values (%s)', _make_tuple_colors(20))


def create_fake_users(num_users):
    fake_list = []
    for _ in range(num_users):
        first = fake.first_name().lower()
        last = fake.last_name().lower()
        full = f'{first}_{last}'

        fake_list.append(full)
    return fake_list

def add_user_to_group(user, group):
    c.execute(f"CREATE USER {user} password 'xyzzy-1-XYZZY';")
    c.execute(f"ALTER GROUP {group} ADD USER {user};")

# %%
def create_database():
    for schema in tqdm(SCHEMAS):
        create_schema(schema)
    conn.commit()
    for schema in tqdm(SCHEMAS):
        for table in tqdm(TABLES):
            full_table = f'{schema}.{table}'
            create_table(full_table)
            insert_colors_in_table(full_table)
    conn.commit()

    for group in tqdm(GROUPS):
        create_group(group)
        users = create_fake_users(20)
        for user in tqdm(users):
            add_user_to_group(user, group)

    for schema in tqdm(SCHEMA_GROUP_PERMISSIONS):
        groups = SCHEMA_GROUP_PERMISSIONS.get(schema)
        for group in tqdm(groups):
            grant_usage_and_select(schema, group)

# %%
c.execute('select * from schema_parts.table_a')
c.fetch_dataframe()

# %% [markdown]
# ## Drop

# %%
# Schemas
def get_all_schemas_to_drop():
    sql = """select distinct schemaname from pg_tables 
        where schemaname not like ('pg_%')
        and schemaname not like ('information_schema');"""
    sql = "select distinct objname from admin.v_generate_user_grant_revoke_ddl where objtype = 'schema';"
    try:
        schemas = [s[0] for s in c.execute(sql).fetchall()]
    except UnicodeDecodeError:
        schemas = [s[0] for s in c.execute(sql).fetchall()]
    return schemas


def drop_schema(schema):
    try:
        c.execute(f"drop schema if exists {schema} cascade;")
    except Exception as e:
        print(f'Error dropping schema {schema}')
        print(e)


# Groups
def get_all_groups_to_drop():
    sql = "select distinct groname from pg_group;"
    try:
        groups = [g[0] for g in c.execute(sql).fetchall()]
    except UnicodeDecodeError:
        groups = [g[0] for g in c.execute(sql).fetchall()]
    return groups


def revoke_group_schema_permissions(group, schema):
    sql = f"revoke all on schema {schema} from group {group};"
    try:
        c.execute(sql)
    except Exception as e:
        print(f'Error revoking schema permissions for {group} on schema {schema}')
        print(e)


def revoke_group_table_permissions(group, schema):
    sql = f"revoke all on all tables in schema {schema} from group {group};"
    try:
        c.execute(sql)
    except Exception as e:
        print(f'Error revoking table permissions for {group} on schema {schema}')
        print(e)


def revoke_group_column_permissions(group, schema):
    pass


def drop_group(group):
    try:
        c.execute(f"drop group {group};")
    except Exception as e:
        print(f'Error dropping group {group}')
        print(e)


# Users
def get_all_users_to_drop():
    try:
        all_users = c.execute('select usename from pg_user;').fetchall()
    except UnicodeDecodeError:
        all_users = c.execute('select usename from pg_user;').fetchall()
    protected_users = ['chris-birch-admin', 'rdsdb', 'cbadmin']
    new_owner = 'cbadmin'
    users_to_drop = [user[0] for user in all_users if user[0] not in protected_users]
    return users_to_drop


def change_ownership(user, new_owner):
    sql = f"select schemaname, tablename from pg_tables where tableowner like '{user}';"
    tables = c.execute(sql).fetchall()
    for table in tables:
        alter_sql = f"alter table {table[0]}.{table[1]} owner to '{new_owner}';"
        try:
            c.execute(alter_sql)
        except Exception as e:
            print(f'Error changing ownership for {table[0]}.{table[1]} owned by {user}')
            print(e)


def revoke_user_schema_permissions(user):
    sql = f"select distinct schemaname from admin.v_get_obj_priv_by_user where usename like '{user}';"
    schemas = [s[0] for s in c.execute(sql).fetchall()]
    for schema in schemas:
        revoke_permissions = f"revoke all on schema {schema} from {user};"
        try:
            c.execute(revoke_permissions)
        except Exception as e:
            print(f'Error revoking schema permissions for {user} on schema {schema}')
            print(e)


def revoke_user_table_permissions(user):
    sql = f"select distinct schemaname from admin.v_get_obj_priv_by_user where usename like '{user}';"
    schemas = [s[0] for s in c.execute(sql).fetchall()]
    for schema in schemas:
        revoke_permissions = f"revoke all on all tables in schema {schema} from {user};"
        try:
            c.execute(revoke_permissions)
        except Exception as e:
            print(f'Error revoking table permissions for {user} on schema {schema}')
            print(e)


def revoke_user_column_permissions(user):
    pass


def drop_user(user):
    try:
        c.execute(f'drop user {user};')
    except Exception as e:
        print(f'Error dropping user {user}')
        print(e)


# %%
def reset_database():
    schemas = get_all_schemas_to_drop()
    groups = get_all_groups_to_drop()
    users = get_all_users_to_drop()

    print('Schemas')
    print(schemas)
    print('Groups')
    print(groups)
    print('Users')
    print(users)

    if groups:
        for group in tqdm(groups):
            if schemas:
                for schema in tqdm(schemas):
                    revoke_group_column_permissions(group, schema)
                    revoke_group_table_permissions(group, schema)
                    revoke_group_schema_permissions(group, schema)
            drop_group(group)

    if schemas:
        for schema in tqdm(schemas):
            drop_schema(schema)

    if users:
        for user in tqdm(users):
            print('USER: ', user)
            df(f"""select * from admin.v_find_dropuser_objs 
            where objowner like '{user}';""")
            change_ownership(user=user, new_owner='cbadmin')
            revoke_user_column_permissions(user=user)
            revoke_user_table_permissions(user=user)
            revoke_user_schema_permissions(user=user)
            drop_user(user=user)

# %%
df("""
select tableowner, schemaname, tablename 
from pg_tables 
where tableowner like 'chris-birch-admin';""")

# %% [markdown]
# # Demo
# - https://blog.satoricyber.com/hardening-aws-redshift-security-access-controls-explained

# %% [markdown]
# # Users and Groups

# %%


# %%




# %%
# view assigned roles to users
c.execute("""
SELECT usename AS user_name, groname AS group_name 
FROM pg_user, pg_group
WHERE pg_user.usesysid = ANY(pg_group.grolist)
AND pg_group.groname in (SELECT DISTINCT pg_group.groname from pg_group)
"""
).fetch_dataframe()

# %%
c.execute('select * from pg_group;').fetch_dataframe()

# %%
c.execute('select nspname from pg_catalog.pg_namespace;').fetch_dataframe()

# %%
c.execute("select nspname from pg_catalog.pg_namespace where nspname like '%schema' ").fetch_dataframe()

# %%
shipping_table_sql = """
CREATE TABLE sales.orders (
order_id varchar(255), order_checksum int, shipping_firstname varchar(50), 
shipping_middlename varchar(25), shipping_lastname varchar(50), 
shipping_street1 varchar(255), shipping_street2 varchar(255), 
shipping_street3 varchar(255), shipping_zipcode varchar(15), 
shipping_pob varchar(15), shipping_city varchar(50), 
shipping_phone1 varchar(50), shipping_phone2 varchar(50), 
shipping_cellular varchar(50), shipping_hours varchar(50), 
shipping_comments varchar(255), payer_creditcard varchar(19), 
payer_expmonth varchar(2), payer_expyear varchar(4), 
payer_firstname varchar(50), payer_middlename varchar(25), 
payer_lastname varchar(50), payer_street1 varchar(255), 
payer_street2 varchar(255), payer_street3 varchar(255), 
payer_zipcode varchar(15), payer_pob varchar(15), payer_city varchar(50), 
payer_phone1 varchar(50), payer_phone2 varchar(50), payer_cellular varchar(50), 
payer_hours varchar(50), payer_comments varchar(255));
"""
c.execute(shipping_table_sql)

# %%
# create user with read-only access to orders table
c.execute("CREATE USER shipping PASSWORD 'xyzzy-1-XYZZY';")
c.execute("GRANT SELECT ON sales.orders TO shipping;")

# %% [markdown]
# ## Column Level Security

# %%
# Revoking the existing SELECT privilege on the entire table
c.execute("REVOKE SELECT ON sales.orders FROM shipping;")
# Granting SELECT privilege specifically to all columns except for the forbidden ones
c.execute("""
GRANT SELECT(order_id, order_checksum, shipping_firstname, 
shipping_middlename, shipping_lastname, shipping_street1,
shipping_street2, shipping_street3, shipping_zipcode, shipping_pob, 
shipping_city, shipping_phone1, shipping_phone2, shipping_cellular, 
shipping_hours, shipping_comments, payer_firstname, payer_middlename,
payer_lastname, payer_street1, payer_street2, payer_street3, payer_zipcode, 
payer_pob, payer_city, payer_phone1, payer_phone2, payer_cellular, 
payer_hours, payer_comments)
ON sales.orders TO shipping"""
)


# %%
c.execute("""
REVOKE SELECT(order_id, order_checksum, shipping_firstname, 
shipping_middlename, shipping_lastname, shipping_street1,
shipping_street2, shipping_street3, shipping_zipcode, shipping_pob, 
shipping_city, shipping_phone1, shipping_phone2, shipping_cellular, 
shipping_hours, shipping_comments, payer_firstname, payer_middlename,
payer_lastname, payer_street1, payer_street2, payer_street3, payer_zipcode, 
payer_pob, payer_city, payer_phone1, payer_phone2, payer_cellular, 
payer_hours, payer_comments)
ON sales.orders FROM shipping"""
)

# %% [markdown]
# ## Row Level Security

# %%
c.execute("""
CREATE TABLE department_employees (
id int,
name varchar(50),
phone varchar(50),
salary smallint,
department varchar(50));
""")

c.execute("""
INSERT INTO department_employees VALUES
(1, 'Seller McSeller', '+1-212-5555555', 180, 'sales'),
(2, 'Sir Sell-A-Lot', '+1-212-5556666', 240, 'sales'),
(3, 'Marky McMarket', '+1-716-5555555', 210, 'marketing'),
(4, 'Sir Market-A-Lot', '+1-716-5556666', 270, 'marketing');
""")

# %%
c.execute("""
CREATE TABLE users_to_groups
(user_name varchar(100), group_name varchar(100));
""")

c.execute("""
INSERT INTO users_to_groups VALUES
('marketing_accountant', 'marketing');
""")

# Let's also create an accountant user
c.execute("""
CREATE USER marketing_accountant WITH PASSWORD 'xyzzy-1-XYZZY';
""")

# %%
c.execute("SELECT * FROM department_employees WHERE department IN (SELECT group_name FROM users_to_groups WHERE user_name='marketing_accountant')").fetch_dataframe()

# %%
c.execute("""
CREATE VIEW v_department_employees AS
SELECT * FROM department_employees
WHERE department IN (SELECT group_name FROM users_to_groups WHERE user_name=CURRENT_USER);
""")

# %%

# Granting access to the user in views
c.execute("GRANT SELECT ON users_to_groups TO marketing_accountant;")
c.execute("GRANT SELECT ON v_department_employees TO marketing_accountant;")


# %%

# Switching to use the context of the user 'marketing_accountant'
c.execute("SET SESSION AUTHORIZATION marketing_accountant;")
c.execute("SELECT * FROM department_employees;").fetchall()

#  We get a permission denied error, as we don't have access to the table itself:
#  Invalid operation: permission denied for relation department_employees


# %%

# We now get the filtered rows */
c.execute("SELECT * FROM v_department_employees;").fetch_dataframe()

# %%
c.execute("SET SESSION AUTHORIZATION 'cbadmin';")
c.execute("SELECT * FROM department_employees;").fetch_dataframe()

# %% [markdown]
# ## Authorization

# %%
# look for failed logins
c.execute("""
SELECT *
FROM stl_connection_log
WHERE event='authentication failure'
ORDER BY recordtime;
""").fetch_dataframe()

# %%
# successful auth by hour, exclude rdsdb
c.execute("""
SELECT DATE_PART(YEAR, recordtime) || '-' ||
	LPAD(DATE_PART(MONTH, recordtime),2,'0') || '-' ||
	LPAD(DATE_PART(DAY, recordtime),2,'0') || ' ' ||
	LPAD(DATE_PART(HOUR, recordtime),2,'0') AS hour_bucket, username, COUNT(*)
FROM stl_connection_log
WHERE event = 'authenticated'
AND username != 'rdsdb'
GROUP BY 1, 2
ORDER BY 1, 2 DESC;
""").fetch_dataframe()

# %%
# show successful auth by number of auth
c.execute("""
SELECT username, event, COUNT(*)
FROM stl_connection_log
WHERE event = 'authenticated'
GROUP BY 1, 2
ORDER BY 3 DESC;
""").fetch_dataframe()

# %%
# connection drivers used
c.execute("""
SELECT username, application_name, COUNT(*) 
FROM stl_connection_log
WHERE application_name != ''
GROUP BY 1,2
ORDER BY 1,2;
""").fetch_dataframe()

# %%
c.execute("""
SELECT * FROM STL_QUERY
LIMIT 100;
""").fetch_dataframe()

# %%
# view permissions for 'user' on 'schema'
c.execute("""
SELECT
    u.usename,
    s.schemaname,
    has_schema_privilege(u.usename,s.schemaname,'create') AS create_permission,
    has_schema_privilege(u.usename,s.schemaname,'usage') AS usage_permission
FROM
    pg_user u
CROSS JOIN
    (SELECT DISTINCT schemaname FROM pg_tables) s
WHERE
    u.usename = 'cbadmin'
    AND s.schemaname = 'second_schema';
""").fetch_dataframe()

# %%
# User Permissions
c.execute("""
SELECT
    u.usename,
    s.schemaname,
    has_schema_privilege(u.usename,s.schemaname,'create') AS create_permission,
    has_schema_privilege(u.usename,s.schemaname,'usage') AS usage_permission
FROM
    pg_user u
CROSS JOIN
    (SELECT DISTINCT schemaname FROM pg_tables
     where schemaname not like 'pg_%'
     and schemaname not like 'information_schema') s;
""").fetch_dataframe()


