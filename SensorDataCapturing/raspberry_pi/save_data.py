import sys
import time
import json
import sqlite3

class Save:
    def __init__(self):
        self.db = 'sensordb.db'
    
    def insert_sensor_data(self,data):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        table_list = cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='sensor_data'; """).fetchall()
        
        if table_list == []:
            print("Creating Table...")
            cur.execute(
                """CREATE TABLE sensor_data(
                        BASE_NAME VARCHAR(255) NOT NULL,
                        DT DOUBLE NOT NULL,
                        TEMP DOUBLE,
                        TEMP_UNIT Char(1),
                        HUM DOUBLE,
                        HUM_UNIT Char(1),
                        SOIL DOUBLE,
                        SOIL_UNIT Char(1),
                        Sent BIT NOT NULL DEFAULT 0,
                        CONSTRAINT ID PRIMARY KEY (BASE_NAME, DT)) ;""")
            
        base = data[0]['bn']
        print("Testbase:")
        print(base)
        epoch_time = float(time.time())

        cur.execute("""INSERT INTO sensor_data(
                        BASE_NAME, DT, TEMP,TEMP_UNIT, HUM, HUM_UNIT, SOIL, SOIL_UNIT)
                        VALUES (?,?,?,?,?,?,?,?);""",
                    (data[0]['bn'],epoch_time, data[0]['v'],data[0]['u'],
                     data[1]['v'],data[1]['u'],
                     data[2]['v'],data[2]['u']))
        print("Data inserted")
        con.commit()
        con.close()
        




