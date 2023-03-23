
# -*- coding: utf-8 -*-
"""
ITM 360: Advanced Application Development

Project: Camper Relationship Management System
         Data - Model

Author: Andrew Minkswinberg
"""

import sqlite3
from datetime import date
from sql import (CREATE_CAMPER_TABLE_SQL, CREATE_INVOICE_TABLE_SQL, CREATE_BUNKHOUSE_TABLE_SQL,
                 CREATE_CAMPER_BUNKHOUSE_TABLE_SQL, CREATE_TRIBE_TABLE_SQL, CREATE_CAMPER_TRIBE_TABLE_SQL,
                 CREATE_LOGIN_TABLE_SQL)



class DatabaseUti:
    def __init__(self, db_name = "Gila.db"):
        self.db = db_name
        self._create_table(CREATE_CAMPER_TABLE_SQL)
        self._create_table(CREATE_INVOICE_TABLE_SQL)
        self._create_table(CREATE_BUNKHOUSE_TABLE_SQL)
        self._create_table(CREATE_CAMPER_BUNKHOUSE_TABLE_SQL)
        self._create_table(CREATE_TRIBE_TABLE_SQL)
        self._create_table(CREATE_CAMPER_TRIBE_TABLE_SQL)
        self._create_table(CREATE_LOGIN_TABLE_SQL)

    def create_connection(self):
        """
        create a database connection to the sqlit database
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except Exception as e:
            print(e)
    
    
    def _create_table(self, create_table_sql):
        
        conn = self.create_connection()
        c = conn.cursor()
        
        try:
            c.execute(create_table_sql)
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

               
    def insert_one_record(self, table_name, values):
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute("""INSERT INTO %s VALUES %s""" %(table_name, values))
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return False
    
    
    def insert_many_records(self, table_name, value_list):
        if table_name in ["camper", "invoice", "bunkhouse", "tribe"]:
            place_holder = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        elif table_name == "camper_bunkhouse":
            place_holder = "(?, ?, ?, ?)"
        elif table_name == "camper_tribe":
            place_holder = "(?, ?, ?, ?)"
        elif table_name == "logins":
            place_holder = "(?, ?, ?)"

        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.executemany(f"INSERT INTO {table_name} VALUES {place_holder}", value_list)
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return False


    def update_camper_table(self, CamperID, FirstName, LastName, Birthday, Gender, ArrivalDate, Equipment, DepartureDate, CompletedForm, CheckedIn, MailingAddress, Friends):
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute(f"""UPDATE camper SET  
                        FirstName = ?,
                        LastName = ?,
                        Birthday = ?,
                        Gender = ?,
                        ArrivalDate = ?,
                        Equipment = ?,
                        DepartureDate = ?,
                        CompletedForm = ?,
                        CheckedIn = ?,
                        MailingAddress = ?,
                        Friends = ?
                        WHERE CamperID = ?""",
                    (FirstName, LastName, Birthday, Gender, ArrivalDate, Equipment, DepartureDate, CompletedForm, CheckedIn, MailingAddress, Friends, CamperID))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return False


    def query_table(self, table_name, field_name):

        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT %s FROM %s" % (field_name, table_name))
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(e)


    def query_table_with_condition(self, table_name, field_name, conditions):
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute("""SELECT %s FROM %s WHERE %s""" % (field_name,
                                                          table_name, conditions))
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(e)

    def check_login(self, username, password):
        conditions = f"username = '{username}'"
        result = self.query_table_with_condition("logins", "password", conditions)
        if len(result) == 0:
            return False
        elif result[0][0] == password:
            return True
        else:
            return False

    
db = DatabaseUti()
# db.insert_one_record("logins", ("admin", "1234"))
