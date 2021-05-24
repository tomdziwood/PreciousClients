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
            if cust.own_or_rent == 'R':
                parameters = (cust.id, cust.firstname, cust.lastname, cust.street_address, cust.district, cust.voivodship,
                              cust.postcode, cust.est_income/2, cust.own_or_rent, cust.date)
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


def calculate_b_transactions(c, insert):
    cur = c.cursor()
    query = '''SELECT C.custid, C.firstname, C.lastname, C.street_address, C.district,
               C.voivodship, C.postcode, SUM(price*quantity) AS purchases FROM B_TRANSACTIONS LEFT JOIN B_CUSTOMERS AS C ON B_TRANSACTIONS.custid = C.custid
               GROUP BY C.custid'''
    cur.execute(query)
    data_b = cur.fetchall()
    if insert is True:
        fields_b = ','.join('?' for desc in cur.description)
        stmt = "insert into {} values ({})".format('AB_CONNECTED', fields_b)
        cur.executemany(stmt, data_b)
        c.commit()
    for row in data_b:
        print(row)
    return cur


def calculate_a_transactions(c, insert):
    cur = c.cursor()

    #sum of purchases
    query_pur = '''SELECT F.lname, SUM(quantity*price*(100-discount)*0.01)
                   FROM A_TRANSACTIONS LEFT JOIN A_CUSTOMERS AS F ON A_TRANSACTIONS.custid = F.custid
                   WHERE transtype = 'PUR'
                   GROUP BY F.custid'''

    #sum of returns
    query_ret = '''SELECT G.lname, SUM(price)
                   FROM A_TRANSACTIONS LEFT JOIN A_CUSTOMERS AS G ON A_TRANSACTIONS.custid = G.custid
                   WHERE transtype = 'RET'
                   GROUP BY G.custid'''

    #purchases-returns
    query = '''SELECT H.custid, H.fname, H.lname, H.street_address, H.district, H.voivodship,
               H.postcode, pur - IFNULL(ret, 0) as purchases              
               FROM (SELECT F.custid, F.fname, F.lname, F.street_address, F.district, F.voivodship,
               F.postcode, F.preferred, SUM(quantity*price*(100-discount)*0.01) as pur               
                     FROM A_TRANSACTIONS LEFT JOIN A_CUSTOMERS AS F ON A_TRANSACTIONS.custid = F.custid
                     WHERE transtype = 'PUR'
                     GROUP BY F.custid) AS H left join (
                        SELECT G.custid, G.lname, SUM(price) as ret
                        FROM A_TRANSACTIONS LEFT JOIN A_CUSTOMERS AS G ON A_TRANSACTIONS.custid = G.custid
                        WHERE transtype = 'RET'
                        GROUP BY G.custid) AS I ON H.custid = I.custid'''
    cur.execute(query)
    data_a = cur.fetchall()
    if insert is True:
        fields_a = ','.join('?' for desc in cur.description)
        stmt = "insert into {} values ({})".format('AB_CONNECTED', fields_a)
        cur.executemany(stmt, data_a)
        c.commit()
    for row in data_a:
        print(row)
    return cur


def select_from_customerinfo(c):
    cur = c.cursor()
    query = '''SELECT id, firstname, lastname, street_address, district, voivodship, postcode, est_income, 
               own_or_rent FROM C_CUSTOMERINFO'''
    cur.execute(query)
    rows = cur.fetchall()
    # for row in rows:
    #     print(row)
    return cur


def create_table_for_cursor_a_and_cursor_b(c):
    c.execute('''CREATE TABLE IF NOT EXISTS AB_CONNECTED
                 (custid number PRIMARY KEY, firstname varchar, lastname varchar, street_address varchar[100], district varchar, 
                 voivodship varchar, postcode number, purchases number)''')
    return


def join_cursor_a_with_cursor_b(c, cur_a, cur_b):
    cursor = c.cursor()
    data_a = cur_a.fetchall()
    data_b = cur_b.fetchall()
    fields_a = ','.join('?' for desc in cur_a.description)
    fields_b = ','.join('?' for desc in cur_b.description)

    stmt = "insert into {} values ({})".format('AB_CONNECTED', fields_a)
    cursor.executemany(stmt, data_a)
    stmt = "insert into {} values ({})".format('AB_CONNECTED', fields_b)
    cursor.executemany(stmt, data_b)
    c.commit()



# Info: zdarza ta sama osoba z innym id w jednym pliku, np. w A
# osoba o nazwisku 'AU' ma dwa idki
# TODO: Insert data from all returned cursors to one table
# TODO: Parammetrize function to find best customers
# TODO: Test solution
