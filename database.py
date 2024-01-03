import sqlite3 as db
from prettytable import PrettyTable


class DataBase:
    def __init__(self):
        self.con = db.connect("Assets/database.db")
        self.c = self.con.cursor()

    def createTable(self):
        self.c.execute("""
        CREATE TABLE  IF NOT EXISTS Weather(
            id text PRIMARY KEY,
            location TEXT ,
            temperature REAL,
            humidity REAL,
            weather_condition TEXT,
            wind_speed REAL,
            visibility REAL,
            Pressure REAL);
             """)
        self.con.commit()

    def insertData(self, date, loc, tem, hum, des, wind_speed, vis, pressure):
        """date loc tem hum des.
        wind vis pres"""
        self.c.execute(f"""
        insert into Weather values(?,?,?,?,?,?,?,?)
        """, (date, loc, tem, hum, des, wind_speed, vis, pressure))
        self.con.commit()

    def deleteAllRecords(self):
        self.c.execute("""
        delete from Weather
        """)
        # self.c.execute("""
        # drop table Weather
        # """)
        self.con.commit()

    def viewData(self):
        data = self.c.execute(f"""
                  select * from Weather 
                  """)
        table = PrettyTable()
        table.field_names = [i[0] for i in self.c.description]  # Set column names
        for row in data.fetchall():
            table.add_row(row)
        print(table)
        self.con.commit()

    def showTableDescription(self):
        data = self.c.execute("""
        PRAGMA table_info(Weather)
        """)
        print(data.fetchall())

    def queryDataByDate(self):
        date = input("Enter the date in dd-mm-yy format: ")
        query = f"""select * from Weather where id like ?"""
        res = self.c.execute(query, (f'%{date}%',))
        print(res.fetchall())

    def close(self):
        self.con.close()

