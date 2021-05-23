import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_tables(c):
    c.execute('''CREATE TABLE IF NOT EXISTS A_CUSTOMERS
                 (custid number PRIMARY KEY, fname varchar, lname varchar, street_address varchar[100], district varchar, 
                 voivodship varchar, postcode number, preferred number)''')

    c.execute('''CREATE TABLE IF NOT EXISTS A_TRANSACTIONS
                 (transid number PRIMARY KEY, transtype varchar, transdate date, custid number, prodid varchar, 
                 quantity number, price number, discount number, returnid number, reason varchar,
                 FOREIGN KEY (custid) REFERENCES A_CUSTOMERS (custid))''')

    c.execute('''CREATE TABLE IF NOT EXISTS B_CUSTOMERS
                 (custid number PRIMARY KEY, firstname varchar, lastname varchar, street_address varchar, 
                 district varchar, voivodship varchar, postcode number)''')

    c.execute('''CREATE TABLE IF NOT EXISTS B_TRANSACTIONS
                 (transid number PRIMARY KEY, prodid varchar, price number, quantity number, transdate date, 
                 custid number, FOREIGN KEY (custid) REFERENCES B_CUSTOMERS (custid))''')

    c.execute('''CREATE TABLE IF NOT EXISTS C_CUSTOMERINFO
                 (id number PRIMARY KEY, firstname varchar, lastname string, street_address varchar, 
                 district varchar, voivodship varchar, postcode number, est_income number, own_or_rent varchar,
                 cdate date, newline varchar)''')
    return


def insert_data_into_table(list, table, c):
    """ add to table
    :param table: decide to which table add list of objects
    :param list: list of objects made from file
    """
    if table == 'A_CUSTOMERS':
        for cust in list:
            query = '''INSERT INTO A_CUSTOMERS (custid, fname, lname, street_address, district, voivodship, postcode, preferred)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?);'''
            parameters = (cust.custid, cust.fname, cust.lname, cust.street_address, cust.district, cust.voivodship,
                          cust.postcode, cust.preferred)
            c.execute(query, parameters)
            c.commit()
    elif table == 'A_TRANSACTIONS':
        for trans in list:
            query = '''INSERT INTO A_TRANSACTIONS (transid, transtype, transdate, custid, prodid, quantity, price, discount, returnid, reason)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
            parameters = (trans.transid, trans.transtype, trans.transdate, trans.custid, trans.prodid, trans.quantity, trans.price, trans.discount, trans.returnid, trans.reason)
            c.execute(query, parameters)
            c.commit()
    elif table == 'B_CUSTOMERS':
        for cust in list:
            query = '''INSERT INTO B_CUSTOMERS (custid, firstname, lastname, street_address, district, voivodship, postcode)
                     VALUES(?, ?, ?, ?, ?, ?, ?);'''
            parameters = (cust.custid, cust.firstname, cust.lastname, cust.street_address, cust.district, cust.voivodship,
                          cust.postcode)
            c.execute(query, parameters)
            c.commit()
    elif table == 'B_TRANSACTIONS':
        for trans in list:
            query = '''INSERT INTO B_TRANSACTIONS (transid, prodid, price, quantity, transdate, custid)
                     VALUES(?, ?, ?, ?, ?, ?);'''
            parameters = (trans.transid, trans.prodid, trans.price, trans.quantity, trans.transdate, trans.custid)
            c.execute(query, parameters)
            c.commit()
    elif table == 'C_CUSTOMERINFO':
        for cust in list:
            query = '''INSERT INTO C_CUSTOMERINFO (id, firstname, lastname, street_address, district, voivodship, postcode, est_income, own_or_rent, cdate)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
            parameters = (cust.id, cust.firstname, cust.lastname, cust.street_address, cust.district, cust.voivodship,
                          cust.postcode, cust.est_income, cust.own_or_rent, cust.date)
            c.execute(query, parameters)
            c.commit()
    else:
        pass
    return


def test_join(c):
    cur = c.cursor()
    query = '''SELECT * FROM A_TRANSACTIONS LEFT JOIN A_CUSTOMERS ON A_TRANSACTIONS.custid = A_CUSTOMERS.custid'''
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return


