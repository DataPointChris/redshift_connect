import argparse
import pathlib
from redshift_connection import RedshiftConnection


parser = argparse.ArgumentParser(
    description="Enter a filename in sql folder.  Returns 'name.csv' in csv folder"
)
parser.add_argument('-f', '--filename')
args = parser.parse_args()
filename = args.filename
sql_file_path = pathlib.Path(f'sql/{filename}')
basename = sql_file_path.stem

print('Connecting to Redshift')
cnxn = RedshiftConnection().connect()
cursor = cnxn.cursor()

with open(sql_file_path, 'r') as query:
    sql = query.read()

print(f'Executing: `{filename}`')
df = cursor.execute(sql).fetch_dataframe()
df.to_csv(f'csv/{basename}.csv')
print(f'Done:  Saved `{filename}` in csv folder.')
