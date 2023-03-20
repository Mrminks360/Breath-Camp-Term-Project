# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:25:07 2023

@author: hzhang
"""

CREATE_LOGIN_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS logins(
                      username text, 
                      password text,
                      UNIQUE(username)) 
                      """

# CREATE_CUSTOMERS_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS customers (
#                                 first_name text NOT NULL, 
#                                 last_name text NOT NULL,
#                                 gender text, 
#                                 date_of_birth text, 
#                                 mobile text,
#                                 address text,
#                                 city text, 
#                                 state text, 
#                                 zipcode text,
#                                 email text UNIQUE,
#                                 registration_date text 
#                                 )
#                               """


CREATE_CUSTOMERS_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS customers (
                                first_name text NOT NULL, 
                                last_name text NOT NULL,
                                gender text, 
                                date_of_birth text, 
                                payment text,
                                family_friends text,
                                equipment boolean,
                                forms boolean,
                                address text,
                                city text, 
                                state text, 
                                zipcode text,
                                email text UNIQUE,
                                registration_date text 
                                )
                              """
CREATE_PAYMENTS_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS payments(
                              transaction_id integer PRIMARY KEY,
                              email text, 
                              payment_date text,
                              payment_amount text,
                              FOREIGN KEY(email) REFERENCES customers(email))
                           """ 