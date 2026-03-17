from mysql.connector import connect, errors
import os


class MysqlConnection:
    def __init__(self, host, port, password, user, database, logger):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.database = database
        self.logger = logger

    def connect(self):
        try:
            self.con = connect(
                host = self.host,
                port = self.port,
                password = self.password,
                user = self.user,
                database = self.database
            )
            self.cursor = self.con.cursor()
            self.logger.info(f"connection with mysql established")
        except errors.Error as e:
            self.logger.error(f"error connecting to mysql: {e}")

    def get(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.logger.info(f"recieved: {result}")
            return result
        except Exception as e:
            self.logger.error(f"error retrieving data: {e}")


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
# )

# query = """
# SELECT * FROM targets;
# """
# a = MysqlConnection(
#     host="localhost",
#     port=3306,
#     password="root",
#     user="root",
#     database="digital_hunter",
#     logger=logging.getLogger("asdf")
# )
# a.connect()
# a.get(query=query)