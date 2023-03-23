# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:25:07 2023

@author: Andrew Minks
"""

CREATE_CAMPER_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS camper (
    CamperID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Birthday DATE NOT NULL,
    Gender TEXT NOT NULL,
    ArrivalDate DATE NOT NULL,
    Equipment TEXT,
    DepartureDate DATE NOT NULL,
    CompletedForm BOOLEAN NOT NULL,
    CheckedIn BOOLEAN NOT NULL,
    MailingAddress TEXT NOT NULL,
    Friends INTEGER,
    FOREIGN KEY (Friends) REFERENCES camper (CamperID)
);
"""

CREATE_INVOICE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS invoice (
    InvoiceID INTEGER PRIMARY KEY,
    CamperID INTEGER NOT NULL,
    Amount REAL NOT NULL,
    Paid BOOLEAN NOT NULL,
    PaymentDate DATE NOT NULL,
    FOREIGN KEY (CamperID) REFERENCES camper (CamperID)
);
"""

CREATE_BUNKHOUSE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bunkhouse (
    BunkhouseID INTEGER PRIMARY KEY,
    BunkhouseName TEXT NOT NULL,
    BunkhouseLocation TEXT NOT NULL
);
"""

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

CREATE_TRIBE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tribe (
    TribeID INTEGER PRIMARY KEY,
    TribeName TEXT NOT NULL,
    TribeLocation TEXT NOT NULL
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

CREATE_LOGIN_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS logins(
                      username text, 
                      password text,
                      UNIQUE(username)) 
                      """
########





# CREATE_CAMPER_TABLE_SQL = """
# CREATE TABLE IF NOT EXISTS camper (
#     CamperID INTEGER PRIMARY KEY AUTO_INCREMENT,
#     FirstName TEXT NOT NULL,
#     LastName TEXT NOT NULL,
#     Birthday DATE NOT NULL,
#     Gender TEXT NOT NULL,
#     ArrivalDate DATE NOT NULL,
#     Equipment TEXT,
#     DepartureDate DATE NOT NULL,
#     CompletedForm BOOLEAN NOT NULL,
#     CheckedIn BOOLEAN NOT NULL,
#     MailingAddress TEXT NOT NULL,
#     Friends INTEGER,
#     FOREIGN KEY (Friends) REFERENCES camper (CamperID)
# );
# """

# CREATE_INVOICE_TABLE_SQL = """
# CREATE TABLE IF NOT EXISTS invoice (
#     InvoiceID INTEGER PRIMARY KEY AUTO_INCREMENT,
#     CamperID INTEGER NOT NULL,
#     Amount REAL NOT NULL,
#     Paid BOOLEAN NOT NULL,
#     PaymentDate DATE NOT NULL,
#     FOREIGN KEY (CamperID) REFERENCES camper (CamperID)
# );
# """

# CREATE_BUNKHOUSE_TABLE_SQL = """
# CREATE TABLE IF NOT EXISTS bunkhouse (
#     BunkhouseID INTEGER PRIMARY KEY AUTO_INCREMENT,
#     BunkhouseName TEXT NOT NULL,
#     BunkhouseLocation TEXT NOT NULL
# );
# """

# CREATE_TRIBE_TABLE_SQL = """
# CREATE TABLE IF NOT EXISTS tribe (
#     TribeID INTEGER PRIMARY KEY AUTO_INCREMENT,
#     TribeName TEXT NOT NULL,
#     TribeLocation TEXT NOT NULL
# );
# """

# CREATE_LOGIN_TABLE_SQL = """
# CREATE TABLE IF NOT EXISTS logins (
#     username TEXT NOT NULL UNIQUE,
#     password TEXT NOT NULL
# );
# """
