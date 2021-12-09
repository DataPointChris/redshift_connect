import argparse
import pandas as pd
import pathlib
from redshift_connection import RedshiftConnection


parser = argparse.ArgumentParser(
    description="Enter '[name]' of a file in sql folder.  Returns '[name].csv' in csv folder"
)
parser.add_argument('-f', '--filename')
args = parser.parse_args()
filename = args.filename
sql_file_path = pathlib.Path(f'sql/{filename}')
basename = sql_file_path.stem

print('Connecting to Redshift')
cnxn = RedshiftConnection().connect()

print(f'Executing: `{filename}`')
with open(sql_file_path, 'r') as query:
    df = pd.read_sql_query(query.read(), con=cnxn)


df.to_csv(f'csv/{basename}.csv')
print(f'Done:  Saved `{filename}` in csv folder.')
