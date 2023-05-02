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
    Friends TEXT NULL,
    AcceptedNotice BOOLEAN DEFAULT 0,
    AcceptedNoticeDate DATE,
    IsCancelled BOOLEAN DEFAULT 0,
    CancellationDate DATE,
    RefundPercentage REAL
);
"""


CREATE_INVOICE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS invoice (
    InvoiceID INTEGER PRIMARY KEY AUTOINCREMENT,
    CamperID INTEGER,
    Amount REAL,
    Paid BOOLEAN,
    PaymentDate DATE,
    RefundAmount REAL,
    FOREIGN KEY (CamperID) REFERENCES camper (CamperID)
);
"""

CREATE_BUNKHOUSE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bunkhouse (
    BunkhouseID INTEGER PRIMARY KEY AUTOINCREMENT,
    BunkhouseName TEXT,
    BunkhouseLocation TEXT,
    BunkhouseGender TEXT
);
"""

CREATE_TRIBE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tribe (
    TribeID INTEGER PRIMARY KEY AUTOINCREMENT,
    TribeName TEXT,
    TribeLocation TEXT
);
"""

########
########
#Bridge Tables

CREATE_CAMPER_BUNKHOUSE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS camper_bunkhouse (
    CamperBunkhouseID INTEGER PRIMARY KEY AUTOINCREMENT,
    CamperID INTEGER,
    BunkhouseID INTEGER,
    BunkhouseUseStartDate DATE,
    BunkhouseUseEndDate DATE,
    FOREIGN KEY (CamperID) REFERENCES camper (CamperID),
    FOREIGN KEY (BunkhouseID) REFERENCES bunkhouse (BunkhouseID)
);
"""

CREATE_CAMPER_TRIBE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS camper_tribe (
    CamperTribeID INTEGER PRIMARY KEY AUTOINCREMENT,
    CamperID INTEGER,
    TribeID INTEGER,
    TribeUseStartDate DATE,
    TribeUseEndDate DATE,
    FOREIGN KEY (CamperID) REFERENCES camper (CamperID),
    FOREIGN KEY (TribeID) REFERENCES tribe (TribeID)
);
"""