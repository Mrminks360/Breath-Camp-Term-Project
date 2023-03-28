# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:25:07 2023

@author: Andrew Minks
"""

# Login 
CREATE_LOGIN_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS logins(
                      username text, 
                      password text,
                      UNIQUE(username)) 
                      """


########
########
#TABLES
CREATE_CAMPER_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS camper (
    CamperID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT,
    LastName TEXT,
    Birthday DATE,
    Gender TEXT,
    ArrivalDate DATE,
    Equipment BOOLEAN,
    DepartureDate DATE,
    CompletedForm BOOLEAN,
    CheckedIn BOOLEAN,
    MailingAddress TEXT,
    Friends TEXT
);
"""

CREATE_INVOICE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS invoice (
    InvoiceID INTEGER PRIMARY KEY AUTOINCREMENT,
    CamperID INTEGER NOT NULL,
    Amount REAL NOT NULL,
    Paid BOOLEAN NOT NULL,
    PaymentDate DATE NOT NULL,
    FOREIGN KEY (CamperID) REFERENCES camper (CamperID)
);
"""

CREATE_BUNKHOUSE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bunkhouse (
    BunkhouseID INTEGER PRIMARY KEY AUTOINCREMENT,
    BunkhouseName TEXT NOT NULL,
    BunkhouseLocation TEXT NOT NULL
);
"""

CREATE_TRIBE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tribe (
    TribeID INTEGER PRIMARY KEY AUTOINCREMENT,
    TribeName TEXT NOT NULL,
    TribeLocation TEXT NOT NULL
);
"""

########
########
#Bridge Tables

CREATE_CAMPER_BUNKHOUSE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS camper_bunkhouse (
    CamperID INTEGER NOT NULL,
    BunkhouseID INTEGER NOT NULL,
    BunkhouseCapacity INTEGER NOT NULL,
    BunkhouseGender TEXT NOT NULL,
    PRIMARY KEY (CamperID, BunkhouseID),
    FOREIGN KEY (CamperID) REFERENCES camper (CamperID),
    FOREIGN KEY (BunkhouseID) REFERENCES bunkhouse (BunkhouseID)
);
"""

CREATE_CAMPER_TRIBE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS camper_tribe (
    CamperID INTEGER NOT NULL,
    TribeID INTEGER NOT NULL,
    TribeCapacity INTEGER NOT NULL,
    TribeGenderRatio TEXT NOT NULL,
    PRIMARY KEY (CamperID, TribeID),
    FOREIGN KEY (CamperID) REFERENCES camper (CamperID),
    FOREIGN KEY (TribeID) REFERENCES tribe (TribeID)
);
"""