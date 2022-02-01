import sqlalchemy as db

class DBManager:

    def __init__(self):
        config = {
        'host': '****',
        'port': 0000,
        'user': '****',
        'password': '****',
        'database': '******'
        }

        db_user = config.get('user')
        db_pwd = config.get('password')
        db_host = config.get('host')
        db_port = config.get('port')
        db_name = config.get('database')
        
        # specify connection string
        connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
        # connect to database
        self.engine = db.create_engine(connection_str)
        self.connection = self.engine.connect()

        self.metadata = db.MetaData()

    def selectAll(self, name_table='User'):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        query = db.select([table])
        ResultProxy = self.connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        return str(ResultSet)

