import redshift_connector

conn = redshift_connector.connect(
    host='data-warehouse.cwmvoana36md.us-east-2.redshift.amazonaws.com',
    port=5439,
    database='dev',
    user='chris-birch',
    password='tohjec-giskag-Xycso3'
)