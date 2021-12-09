import redshift_connector
import dotenv
import os

dotenv.load_dotenv()


class RedshiftConnection:
    def __init__(self):
        pass

    def connect(self):
        self.conn = redshift_connector.connect(
            host=os.environ.get('HOST'),
            port=int(os.environ.get('PORT')),
            database=os.environ.get('DATABASE'),
            user=os.environ.get('DBUSER'),
            password=os.environ.get('PASSWORD'),
        )
        self.conn.autocommit = True
        return self.conn
