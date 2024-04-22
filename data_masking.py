# %% [markdown]
# # Data Masking

# %%
# Static masking using Views
df("""
CREATE OR REPLACE VIEW redacted_customers AS
SELECT sha2(first_name, 256) AS first_name, 
sha2(last_name, 256) AS last_name, 
country_code,
REGEXP_REPLACE(email, '[^@]+@', '*@') AS email
FROM customers;
""")

# %%
# dynamic masking
df("""
CREATE VIEW v_customers AS
SELECT CASE WHEN CURRENT_USER='admin' THEN first_name ELSE sha2(first_name, 256) END AS first_name,
CASE WHEN CURRENT_USER='admin' THEN last_name ELSE sha2(last_name, 256) END AS last_name,
country_code,
CASE WHEN CURRENT_USER='admin' THEN email ELSE REGEXP_REPLACE(email, '[^@]+@', '*@') END AS email
FROM public.customers;
""")

# %%


# %%



