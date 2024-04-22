# %%
from redshift_connection import RedshiftConnection
conn = RedshiftConnection().connect()
c = conn.cursor()

def df(sql):
    return c.execute(sql).fetch_dataframe()

# %%
def check_schema_exists(schema):
    sql = f"""
    select exists (
      select * from pg_tables
      where schemaname = '{schema}'
    );
    """
    return c.execute(sql).fetchone()[0]

def check_table_exists(schema, table):
    sql = f"""
    select exists (
      select * from pg_tables
      where schemaname = '{schema}'
      and tablename = '{table}'
    );
    """
    return c.execute(sql).fetchone()[0]

# %%
def check_schema_table_exists(schema_tables):
    error_list = []
    for st in schema_tables:
        schema, table = st.split('.')
        schema_exists = check_schema_exists(schema)
        table_exists = check_table_exists(schema, table)
        if not schema_exists:
            error_list.append(f"SCHEMA '{schema}' does not exist.")
            continue
        if schema_exists and not table_exists:
            error_list.append(f"TABLE '{table}' does not exist inside SCHEMA '{schema}'")
    return sorted(list(set(error_list)))

# %%
def get_users_in_security_groups(security_groups):
    for sg in security_groups:
        # get the username column
        pass

def get_users_with_no_security_groups(security_groups):
    for sg in security_groups:
        # get the username column
        pass

# %%
# Data Inventory - manual process
df("""
SELECT column_name, table_name, table_schema, table_catalog
FROM information_schema.columns
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY table_catalog, table_schema, table_name, ordinal_position ;
""")

# %% [markdown]
# ## Permissions

# %%
# user has permissions on specific table
c.execute("""
SELECT * 
FROM 
    (
    SELECT 
        schemaname
        ,objectname
        ,usename
        ,HAS_TABLE_PRIVILEGE(usrs.usename, fullobj, 'select') AND has_schema_privilege(usrs.usename, schemaname, 'usage')  AS sel
        ,HAS_TABLE_PRIVILEGE(usrs.usename, fullobj, 'insert') AND has_schema_privilege(usrs.usename, schemaname, 'usage')  AS ins
        ,HAS_TABLE_PRIVILEGE(usrs.usename, fullobj, 'update') AND has_schema_privilege(usrs.usename, schemaname, 'usage')  AS upd
        ,HAS_TABLE_PRIVILEGE(usrs.usename, fullobj, 'delete') AND has_schema_privilege(usrs.usename, schemaname, 'usage')  AS del
        ,HAS_TABLE_PRIVILEGE(usrs.usename, fullobj, 'references') AND has_schema_privilege(usrs.usename, schemaname, 'usage')  AS ref
    FROM
        (
        SELECT schemaname, 't' AS obj_type, tablename AS objectname, schemaname + '.' + tablename AS fullobj FROM pg_tables
        WHERE schemaname not in ('pg_internal')
        UNION
        SELECT schemaname, 'v' AS obj_type, viewname AS objectname, schemaname + '.' + viewname AS fullobj FROM pg_views
        WHERE schemaname not in ('pg_internal')
        ) AS objs
        ,(SELECT * FROM pg_user) AS usrs
    ORDER BY fullobj
    )
WHERE (sel = true or ins = true or upd = true or del = true or ref = true)
-- and schemaname='third_schema'
-- and objectname='b'
and usename = 'cbadmin';
""").fetch_dataframe()

# %%
# Group Permissions

df("""
select
namespace as schemaname , item as object, pu.groname as groupname
, decode(charindex('r',split_part(split_part(array_to_string(relacl, '|'),pu.groname,2 ) ,'/',1)),0,0,1)  as select
, decode(charindex('w',split_part(split_part(array_to_string(relacl, '|'),pu.groname,2 ) ,'/',1)),0,0,1)  as update
, decode(charindex('a',split_part(split_part(array_to_string(relacl, '|'),pu.groname,2 ) ,'/',1)),0,0,1)  as insert
, decode(charindex('d',split_part(split_part(array_to_string(relacl, '|'),pu.groname,2 ) ,'/',1)),0,0,1)  as delete
from
(select
use.usename as subject,
nsp.nspname as namespace,
c.relname as item,
c.relkind as type,
use2.usename as owner,
c.relacl
from
pg_user use
cross join pg_class c
left join pg_namespace nsp on (c.relnamespace = nsp.oid)
left join pg_user use2 on (c.relowner = use2.usesysid)
where c.relowner = use.usesysid
and  nsp.nspname not in ('pg_catalog', 'pg_toast', 'information_schema')
)
join pg_group pu on array_to_string(relacl, '|') like '%'||pu.groname||'%';
  """)

# %%
# all grant and revoke permissions
df("""
WITH util_cmds AS (
SELECT userid, 
LISTAGG(CASE WHEN LEN(RTRIM(text)) = 0
THEN text
ELSE RTRIM(text)
END) 
WITHIN GROUP (ORDER BY sequence) AS query_statement 
FROM stl_utilitytext GROUP BY userid, xid order by xid)
SELECT util_cmds.userid, stl_userlog.username, query_statement
FROM util_cmds
LEFT JOIN stl_userlog ON (util_cmds.userid = stl_userlog.userid)
WHERE query_statement
ILIKE '%GRANT%' OR query_statement ILIKE '%REVOKE%';
""")

# %% [markdown]
# ## Info

# %%
df('select default_iam_role();')

# %%
df('select user, current_user_id;')

# %%
df('select user, current_aws_account, current_database(), current_schema();')

# %% [markdown]
# ## Audit Logs

# %%
df('select * from stl_connection_log;')

# %%
c.execute("""
select * from stl_userlog;
""").fetch_dataframe()

# %%
c.execute("""
select * from stl_query;
""").fetch_dataframe()

# %%
# Last 10 failed logins
df("""
SELECT *
FROM stl_connection_log
WHERE event='authentication failure'
ORDER BY recordtime DESC 
LIMIT 10;
""")

# %%
# top 10 longest queries
df("""
WITH queries AS (
SELECT query, 
LISTAGG(CASE WHEN LEN(RTRIM(text)) = 0 THEN text ELSE RTRIM(text) END) WITHIN GROUP (ORDER BY sequence) AS query_statement, COUNT(*) as row_count 
FROM stl_querytext
GROUP BY query)
SELECT * FROM queries WHERE query_statement ILIKE 'select%'
ORDER BY LEN(query_statement) DESC 
LIMIT 10;
""")

# %%
# last 10 queries run on the cluster
df("""
SELECT query, 
LISTAGG(CASE WHEN LEN(RTRIM(text)) = 0 THEN text ELSE RTRIM(text) END) WITHIN GROUP (ORDER BY sequence) AS query_statement, COUNT(*) as row_count 
FROM stl_querytext
GROUP BY query
ORDER BY query desc
LIMIT 10;
""")


