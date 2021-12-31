import psycopg2
from datetime import datetime
import logging

class DBAccess(object):
    global conn

    def __init__(self):
        self.logger = logging.getLogger('dbApplication')
        try:
            self.conn = psycopg2.connect(database="postgres", user="dbApplication", password="dbApplication", host="127.0.0.1", port="5432")
        except(Exception, psycopg2.Error) as error:
            self.logger.error(error)

    def CloseConnection(self):
        self.conn.close()

    def QueryData(self,SQL):
        try:
            cur = self.conn.cursor()
            cur.execute(SQL)
            self.conn.commit()
            return cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)

    def InsertData(self,SQL):
        try:
            cur = self.conn.cursor()
            cur.execute(SQL)
            self.conn.commit()
            return cur.rowcount
        except(Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)

    def QueryTransaction(self,SqlList):
        try:
            with self.conn.cursor() as cur:
                for sql in SqlList:
                    cur.execute(sql)
                self.conn.commit()
                return cur.rowcount
        except(Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)

    def backupDb(self):
        try:
            cur = self.conn.cursor()
            f = open(datetime.today().strftime("%Y-%m-%d") + '-backup.sql', 'w')
            tables = self.QueryData("SELECT table_name from information_schema.tables WHERE table_schema = 'mydb'")
            for table in list(tables):
                cur.execute("SELECT * FROM mydb." + table[0] )
                for row in cur:
                    f.write("insert into mydb." + table[0] + " values (" + str(row) + ");")

        except(Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)