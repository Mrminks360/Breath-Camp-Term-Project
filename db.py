import sqlite3
from datetime import date
from sql import (CREATE_CAMPER_TABLE_SQL, CREATE_INVOICE_TABLE_SQL, CREATE_BUNKHOUSE_TABLE_SQL,
                 CREATE_CAMPER_BUNKHOUSE_TABLE_SQL, CREATE_TRIBE_TABLE_SQL, CREATE_CAMPER_TRIBE_TABLE_SQL,
                 CREATE_LOGIN_TABLE_SQL)
from datetime import datetime, date, timedelta
import random

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

    def update_camper_table(self, CamperID, FirstName, LastName, Birthday, Gender, ArrivalDate, Equipment,
                            DepartureDate, CompletedForm, CheckedIn, MailingAddress, Friends, IsActive):
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
                        Friends = ?,
                        IsActive = ?
                        WHERE CamperID = ?""",
                      (FirstName, LastName, Birthday, Gender, ArrivalDate, Equipment, DepartureDate,
                       CompletedForm, CheckedIn, MailingAddress, Friends, IsActive, CamperID))
            
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

    def insert_camper_data_from_file(self, file_path):
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
                accepted_notice = False
                accepted_notice_date = None
                try:
                    c.execute("INSERT INTO camper(FirstName, LastName, Birthday, Gender, ArrivalDate, Equipment, DepartureDate, CompletedForm, CheckedIn, MailingAddress, Friends, AcceptedNotice, AcceptedNoticeDate) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (first_name, last_name, birthday, gender, arrival_date, equipment, departure_date, completed_form, checked_in, mailing_address, friends, accepted_notice, accepted_notice_date))
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

    def query_camper_info(self):
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT CamperID, Gender, Birthday FROM camper")
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(e)

    def compute_age(birthday):
        # Convert the birthday string to a datetime object
        birthdate = datetime.strptime(birthday, '%Y-%m-%d').date()

        # Compute the age based on the current date and the birthdate
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age        
    
    def insert_camper_bunkhouse(self):
        # Get camper info from the database
        camper_info = self.query_camper_info()

        # Sort the campers by age and gender
        sorted_campers = sorted(camper_info, key=lambda camper: (DatabaseUti.compute_age(camper[2]), camper[1]))

        # Divide the campers into female and male lists
        female_campers = [camper[0] for camper in sorted_campers if camper[1] == "Female"]
        male_campers = [camper[0] for camper in sorted_campers if camper[1] == "Male"]

        # Insert campers into the camper_bunkhouse table
        with self.create_connection() as conn:
            cur = conn.cursor()

            # Insert male campers into bunkhouses 1-3
            for i, camper_id in enumerate(male_campers):
                bunkhouse_id = i % 3 + 1
                cur.execute("INSERT INTO camper_bunkhouse (CamperID, BunkhouseID, BunkhouseUseStartDate, BunkhouseUseEndDate) VALUES (?, ?, ?, ?)",
                            (camper_id, bunkhouse_id, "2023-07-01", "2023-07-15"))

            # Insert female campers into bunkhouses 4-6
            for i, camper_id in enumerate(female_campers):
                bunkhouse_id = i % 3 + 4
                cur.execute("INSERT INTO camper_bunkhouse (CamperID, BunkhouseID, BunkhouseUseStartDate, BunkhouseUseEndDate) VALUES (?, ?, ?, ?)",
                            (camper_id, bunkhouse_id, "2023-07-01", "2023-07-15"))
  
    def get_bunkhouse_assignments(self, bunkhouse_id):
            with self.create_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT c.CamperID, c.FirstName, c.LastName, c.Birthday, c.Gender
                    FROM camper c
                    JOIN camper_bunkhouse cb ON c.CamperID = cb.CamperID
                    WHERE cb.BunkhouseID = ?
                    """, (bunkhouse_id,))
                records = cur.fetchall()
            return records

    def check_availability(self, arrival_date, departure_date, gender):
        # Check the number of campers within the given arrival and departure dates
        conditions = f"ArrivalDate <= '{departure_date}' AND DepartureDate >= '{arrival_date}' AND Gender = '{gender}'"
        result = self.query_table_with_condition("camper", "COUNT(*)", conditions)

        # Check if there are available slots
        if result and result[0][0] < 36:
            return True
        else:
            return False

    def get_unnotified_campers(self):
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT CamperID, FirstName, LastName, MailingAddress FROM camper WHERE AcceptedNotice = 0")
            results = c.fetchall()
        except Exception as e:
            print(e)
        conn.close()
        return results

    def update_acceptance_notice(self, camper_id, accepted_notice, accepted_notice_date):
        conn = self.create_connection()
        c = conn.cursor()
        try:
            c.execute("UPDATE camper SET AcceptedNotice = ?, AcceptedNoticeDate = ? WHERE CamperID = ?",
                    (accepted_notice, accepted_notice_date, camper_id))
            conn.commit()
        except Exception as e:
            print(e)
        conn.close()
  
    def remove_camper_from_tribe(self, camper_id):
        try:
            self.cursor.execute("UPDATE Camper SET TribeID = NULL WHERE CamperID = ?", (camper_id,))
            self.conn.commit()
            return True
        except:
            return False

    def get_male_count(self, tribe_id):
        self.cursor.execute("SELECT COUNT(*) FROM Camper WHERE Gender='Male' AND TribeID=?", (tribe_id,))
        count = self.cursor.fetchone()[0]
        return count

    def get_female_count(self, tribe_id):
        self.cursor.execute("SELECT COUNT(*) FROM Camper WHERE Gender='Female' AND TribeID=?", (tribe_id,))
        count = self.cursor.fetchone()[0]
        return count

    def insert_camper_tribe(self):
        camper_info = self.query_camper_info()

        # Group campers by friends value
        friends_dict = {}
        for camper in camper_info:
            friends_val = camper[3]  # Assuming friends column is in index 3
            if friends_val not in friends_dict:
                friends_dict[friends_val] = []
            friends_dict[friends_val].append(camper[0])  # Append camper id

        # Sort campers by age and gender within each friend group
        for friends_group in friends_dict.values():
            sorted_campers = sorted([camper for camper in camper_info if camper[0] in friends_group],
                                    key=lambda camper: (DatabaseUti.compute_age(camper[2]), camper[1]))
            female_campers = [camper[0] for camper in sorted_campers if camper[1] == "Female"]
            male_campers = [camper[0] for camper in sorted_campers if camper[1] == "Male"]

            # Insert campers into tribes
            with self.create_connection() as conn:
                cur = conn.cursor()
                num_tribes = 6
                tribe_capacity = 6
                for tribe_id in range(1, num_tribes + 1):
                    num_male_campers = min(len(male_campers), tribe_capacity // 2)
                    num_female_campers = min(len(female_campers), tribe_capacity // 2)
                    if num_male_campers < tribe_capacity // 2:
                        num_female_campers += min(len(female_campers) - num_female_campers,
                                                  tribe_capacity - num_male_campers - num_female_campers)
                    for i in range(num_male_campers):
                        camper_id = male_campers.pop(0)
                        cur.execute(
                            "INSERT INTO camper_tribe (CamperID, TribeID, TribeUseStartDate, TribeUseEndDate) VALUES (?, ?, ?, ?)",
                            (camper_id, tribe_id, "2023-07-01", "2023-07-15"))
                    for i in range(num_female_campers):
                        camper_id = female_campers.pop(0)
                        cur.execute(
                            "INSERT INTO camper_tribe (CamperID, TribeID, TribeUseStartDate, TribeUseEndDate) VALUES (?, ?, ?, ?)",
                            (camper_id, tribe_id, "2023-07-01", "2023-07-15"))
                    if not male_campers and not female_campers:
                        break

    def get_tribe_assignments(self, tribe_id):
            with self.create_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT c.CamperID, c.FirstName, c.LastName, c.Birthday, c.Gender
                    FROM camper c
                    JOIN camper_tribe ct ON c.CamperID = ct.CamperID
                    WHERE ct.TribeID = ?
                    """, (tribe_id,))
                records = cur.fetchall()
            return records

    def update_records(self, table_name, updated_data, conditions):
        conn = self.create_connection()
        c = conn.cursor()

        update_fields = []
        update_values = []

        for field, value in updated_data.items():
            if value is not None:
                update_fields.append(f"{field} = ?")
                update_values.append(value)

        if not update_fields:
            return False

        update_query = f"UPDATE {table_name} SET {', '.join(update_fields)} WHERE {conditions}"
        try:
            c.execute(update_query, update_values)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return False

db = DatabaseUti()

#  To Recreate database move the data from the data folder into the same folder as db.py or copy the path and put into the functions below.
# db.insert_one_record("logins", ("admin", "1234"))
# db.insert_camper_data_from_file("FemaleCampers.txt")
# db.insert_camper_data_from_file("MaleCampers.txt")
# db.insert_bunkhouse_data_from_file("Bunkhouse.txt")
# db.insert_tribe_data_from_file("Tribe.txt")



