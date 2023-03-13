
# -*- coding: utf-8 -*-
"""
ITM 360: Advanced Application Development

Project: Customer Relationship Management System
         Data - Model

Author: Rachel Z (hzhang@ut.edu)
"""

import sqlite3
from datetime import date
from sql import CREATE_CUSTOMERS_TABLE_SQL, CREATE_PAYMENTS_TABLE_SQL, CREATE_LOGIN_TABLE_SQL


class DatabaseUti:
    def __init__(self, db_name = "cms.db"):
        self.db = db_name
        self._create_table(CREATE_CUSTOMERS_TABLE_SQL)
        self._create_table(CREATE_PAYMENTS_TABLE_SQL)
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
        if table_name == "customers":
            place_holder = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)"
        if table_name == "payments":
            place_holder = "(?, ?, ?)"
            
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.executemany("""INSERT INTO %s VALUES %s""" %(table_name, place_holder), value_list)
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return False

    def update_customer_table(self,f_name, l_name, gender, dob, mobile, address, city, state, zipcode, email):
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute(f"""UPDATE customers SET  
                          first_name = '{f_name}', 
                          last_name = '{l_name}',
                          gender = '{gender}', 
                          date_of_birth = '{dob}', 
                          mobile = '{mobile}', 
                          address = '{address}', 
                          city = '{city}', 
                          state = '{state}',  
                          zipcode = '{zipcode}'
                          WHERE email = '%s'""" %(email))
         
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
db.insert_one_record("logins", ("admin", "1234"))
db.check_login("admin", "1234")
#db.add_login_user("RachelZ", "Rz1234")
#db.add_customer("rachel", 'zhang', 'f', '1988-10-12', '9093446739', '20955 monza loop', 'land o lakes', 'fl', '34638', 'hzhang@ut.edu')
#db.add_customer("rachel", 'zhang', 'f', '1988-10-12', '9093446739', '20955 monza loop', 'land o lakes', 'fl', '34638', 'hengwei.zhang@cgu.edu')
#db.add_payment("hzhang@ut.edu", "2023-01-10", "100")
#db.add_payment("hzhang@ut.edu", "2022-01-01", "100")
#db.add_payment("hengwei.zhang@cgu.edu", "2023-01-10", "100")