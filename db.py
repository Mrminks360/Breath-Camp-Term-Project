
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
from datetime import date


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
            placeholders = ', '.join(['?'] * len(values))
            c.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
            conn.commit()
            conn.close()
            return True  # Record successfully inserted
        except Exception as e:
            print(e)
            return False  # Error occurred, record not inserted
    
    def insert_many_records(self, table_name, value_list):
        if table_name == "camper":
            place_holder = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        elif table_name == "invoice":
            place_holder = "(?, ?, ?, ?)"
        elif table_name == "bunkhouse":
            place_holder = "(?, ?, ?)"
        elif table_name == "tribe":
            place_holder = "(?, ?)"
        elif table_name == "camper_bunkhouse":
            place_holder = "(?, ?, ?, ?)"
        elif table_name == "camper_tribe":
            place_holder = "(?, ?, ?, ?)"
        

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
        
    def update_camper_checkin(self, CamperID, **kwargs):
        conn = self.create_connection()
        c = conn.cursor()

        update_fields = []
        update_values = []

        for field, value in kwargs.items():
            if value is not None:
                update_fields.append(f"{field} = ?")
                update_values.append(value)

        if not update_fields:
            return False

        update_query = f"UPDATE camper SET {', '.join(update_fields)} WHERE CamperID = ?"
        update_values.append(CamperID)

        try:
            c.execute(update_query, update_values)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def insert_camper_data_from_file(self,file_path):
        conn = DatabaseUti().create_connection()
        c = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                data = line.strip().split(";")
                first_name = data[0]
                last_name = data[1]
                birthday = data[2]
                gender = data[3]
                arrival_date = data[4]
                equipment = bool(int(data[5]))
                departure_date = data[6]
                completed_form = bool(int(data[7]))
                checked_in = bool(int(data[8]))
                mailing_address = data[9]
                friends = data[10] if data[10] != "None" else None
                try:
                    c.execute("INSERT INTO camper(FirstName, LastName, Birthday, Gender, ArrivalDate, Equipment, DepartureDate, CompletedForm, CheckedIn, MailingAddress, Friends) VALUES(?,?,?,?,?,?,?,?,?,?,?)", 
                        (first_name, last_name, birthday, gender, arrival_date, equipment, departure_date, completed_form, checked_in, mailing_address, friends))
                except Exception as e:
                    print(e)
        conn.commit()
        conn.close()
    
    def insert_bunkhouse_data_from_file(self,file_path):
        conn = DatabaseUti().create_connection()
        c = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                data = line.strip().split(";")
                bunkhouse_name = data[0]
                bunkhouse_location = data[1]
                bunkhouse_gender = data[2]
                try:
                    c.execute("INSERT INTO bunkhouse(BunkhouseName, BunkhouseLocation, BunkhouseGender) VALUES(?,?,?)", 
                        (bunkhouse_name, bunkhouse_location, bunkhouse_gender))
                except Exception as e:
                    print(e)
        conn.commit()
        conn.close()

    def insert_tribe_data_from_file(self,file_path):
        conn = DatabaseUti().create_connection()
        c = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                data = line.strip().split(";")
                tribe_name = data[0]
                tribe_location = data[1]
                try:
                    c.execute("INSERT INTO tribe(TribeName, TribeLocation) VALUES(?,?)", 
                        (tribe_name, tribe_location))
                except Exception as e:
                    print(e)
        conn.commit()
        conn.close()


db = DatabaseUti()

#  To Recreate database move the data from the data folder into the same folder as db.py or copy the path and put into the functions below.
# db.insert_one_record("logins", ("admin", "1234"))
# db.insert_camper_data_from_file("FemaleCampers.txt")
# db.insert_camper_data_from_file("MaleCampers.txt")
# db.insert_bunkhouse_data_from_file("Bunkhouse.txt")
# db.insert_tribe_data_from_file("Tribe.txt")



