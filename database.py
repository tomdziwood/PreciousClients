import sqlite3
import csv

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
                 (custid number[8] PRIMARY KEY, fname varchar[20], lname varchar[25], street_address varchar[90], district varchar[30], 
                 voivodship varchar[20], postcode number[5], preferred number[1], tabsource char)''')

    c.execute('''CREATE TABLE IF NOT EXISTS A_TRANSACTIONS
                 (transid number[9] PRIMARY KEY, transtype varchar[3], transdate date[6], custid number[8], prodid varchar[8], 
                 quantity number[3], price number[7], discount number[3], returnid number[9], reason varchar[30],
                 FOREIGN KEY (custid) REFERENCES A_CUSTOMERS (custid))''')

    c.execute('''CREATE TABLE IF NOT EXISTS B_CUSTOMERS
                 (custid number PRIMARY KEY, firstname varchar, lastname varchar, street_address varchar, 
                 district varchar, voivodship varchar, postcode number, tabsource char)''')

    c.execute('''CREATE TABLE IF NOT EXISTS B_TRANSACTIONS
                 (transid number PRIMARY KEY, prodid varchar, price number, quantity number, transdate date, 
                 custid number, FOREIGN KEY (custid) REFERENCES B_CUSTOMERS (custid))''')

    c.execute('''CREATE TABLE IF NOT EXISTS C_CUSTOMERINFO
                 (id number[9] PRIMARY KEY, firstname varchar[42], lastname varchar[32], street_address varchar[110], 
                 district varchar[40], voivodship varchar[50], postcode number[5], est_income number[8], own_or_rent varchar[1],
                 cdate date[10], tabsource char)''')
    return


def insert_data_into_table(list, table, c):
    """ add to table
    :param table: decide to which table add list of objects
    :param list: list of objects made from file
    """
    if table == 'A_CUSTOMERS':
        for cust in list:
            query = '''INSERT INTO A_CUSTOMERS (custid, fname, lname, street_address, district, voivodship, postcode, preferred, tabsource)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
            parameters = (cust.custid, cust.fname, cust.lname, cust.street_address, cust.district, cust.voivodship,
                          cust.postcode, cust.preferred, 'A')
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
            query = '''INSERT INTO B_CUSTOMERS (custid, firstname, lastname, street_address, district, voivodship, postcode, tabsource)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?);'''
            parameters = (cust.custid, cust.firstname, cust.lastname, cust.street_address, cust.district, cust.voivodship,
                          cust.postcode, 'B')
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
            query = '''INSERT INTO C_CUSTOMERINFO (id, firstname, lastname, street_address, district, voivodship, postcode, est_income, own_or_rent, cdate, tabsource)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
            parameters = (cust.id, cust.firstname, cust.lastname, cust.street_address, cust.district, cust.voivodship,
                          cust.postcode, cust.est_income, cust.own_or_rent, cust.date, 'C')
            if cust.own_or_rent == 'R':
                parameters = (cust.id, cust.firstname, cust.lastname, cust.street_address, cust.district, cust.voivodship,
                              cust.postcode, cust.est_income/2, cust.own_or_rent, cust.date, 'C')
            c.execute(query, parameters)
            c.commit()
    else:
        pass
    return


def calculate_b_transactions(c, insert):
    cur = c.cursor()
    query = '''SELECT C.custid, C.firstname, C.lastname, C.street_address, C.district,
               C.voivodship, C.postcode, C.tabsource, SUM(price*quantity) AS purchases FROM B_TRANSACTIONS LEFT JOIN B_CUSTOMERS AS C ON B_TRANSACTIONS.custid = C.custid
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
               H.postcode, H.tabsource, pur - IFNULL(ret, 0) as purchases              
               FROM (SELECT F.custid, F.fname, F.lname, F.street_address, F.district, F.voivodship,
               F.postcode, F.preferred, F.tabsource, SUM(quantity*price*(100-discount)*0.01) as pur               
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
               own_or_rent, tabsource FROM C_CUSTOMERINFO'''
    cur.execute(query)
    data_c = cur.fetchall()
    for row in data_c:
        print(row)
    return cur


def create_table_for_cursor_a_and_cursor_b(c):
    c.execute('''CREATE TABLE IF NOT EXISTS AB_CONNECTED
                 (custid number PRIMARY KEY, firstname varchar, lastname varchar, street_address varchar[100], district varchar, 
                 voivodship varchar, postcode number, tabsource number, purchases number)''')
    return


def group_ab_table(c):
    '''Show first_defined id, firstname, lastname and sum of purchases from AB'''
    cur = c.cursor()
    query = '''SELECT MIN(custid), firstname, lastname, SUM(purchases) FROM AB_CONNECTED
               GROUP BY lastname'''
    cur.execute(query)
    data_ab = cur.fetchall()
    for row in data_ab:
        print(row)
    return cur


def create_final_table(c):
    c.execute('''CREATE TABLE IF NOT EXISTS FINAL_TABLE
                 (Id number PRIMARY KEY, Source varchar, Fname varchar, Lname varchar, Street_address varchar[110], District varchar[40],
                  Voivodship varchar[50], postcode varchar[5], Preferred varchar, est_income number, own_or_rent varchar,
                  Purchases number)''')
    return


def insert_into_final_table(c, insert):
    cur = c.cursor()
    #inner join AB & Customerinfo
    query_inner = '''SELECT MIN(custid), AB.tabsource, AB.firstname, AB.lastname, AB.street_address, AB.district, AB.voivodship, AB.postcode,
                     C.est_income, C.own_or_rent, SUM(AB.purchases) FROM AB_CONNECTED AS AB INNER JOIN C_CUSTOMERINFO AS C 
                     ON AB.lastname = C.lastname AND AB.firstname = C.firstname AND AB.street_address = C.street_address
                     AND AB.voivodship = C.voivodship
                     GROUP BY AB.lastname'''
    #customers from AB and not in Customerinfo
    query_ab = '''SELECT AB.custid, AB.tabsource, AB.firstname, AB.lastname, AB.street_address, AB.district, AB.voivodship,
                  AB.postcode, AB.purchases FROM 
                  AB_CONNECTED AS AB LEFT JOIN C_CUSTOMERINFO AS C ON AB.lastname = C.lastname
                  WHERE C.lastname IS NULL'''
    #customers from Customerinfo and not in AB
    query_c = '''SELECT C.id, C.tabsource, C.firstname, C.lastname, C.street_address, C.district, C.voivodship,
                 C.postcode, C.est_income, C.own_or_rent FROM
                 C_CUSTOMERINFO AS C LEFT JOIN AB_CONNECTED AS AB ON AB.lastname = C.lastname
                 WHERE AB.lastname IS NULL'''

    if insert is True:
        cur.execute(query_inner)
        data_inner = cur.fetchall()
        stmt = "INSERT INTO FINAL_TABLE (Id, Source, Fname, Lname, Street_address, District, Voivodship, postcode," \
               "est_income, own_or_rent, Purchases) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.executemany(stmt, data_inner)
        c.commit()

        cur.execute(query_ab)
        data_ab = cur.fetchall()
        stmt = "INSERT INTO FINAL_TABLE (Id, Source, Fname, Lname, Street_address, District, Voivodship, postcode," \
               "Purchases) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.executemany(stmt, data_ab)
        c.commit()

        cur.execute(query_c)
        data_c = cur.fetchall()
        stmt = "INSERT INTO FINAL_TABLE (Id, Source, Fname, Lname, Street_address, District, Voivodship, postcode," \
               "est_income, own_or_rent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.executemany(stmt, data_c)
        c.commit()

    cur.execute(query_inner)
    data_ab = cur.fetchall()
    for row in data_ab:
        print(row)
    return cur


def find_best_customers(c, income_treshold=200000, transaction_treshold=500, vip_income=10900):
    #1769
    cur = c.cursor()

    cur.execute('''UPDATE FINAL_TABLE
                   SET own_or_rent = 'U'
                   WHERE own_or_rent is null''')
    c.commit()

    cur.execute('''UPDATE FINAL_TABLE
                   SET Preferred = 2
                   WHERE (Purchases < ? AND est_income < ?) OR (Purchases is null AND est_income is null) OR
                   (Purchases < ? AND est_income is null) OR (Purchases is null AND est_income < ?)
                   OR est_income > ?''', (transaction_treshold, income_treshold, transaction_treshold, income_treshold, vip_income))
    c.commit()

    cur.execute('''UPDATE FINAL_TABLE
                   SET Preferred = 1
                   WHERE Purchases > ? OR est_income > ?
                   AND est_income < ?''', (transaction_treshold, income_treshold, vip_income))
    c.commit()

    cur.execute('''SELECT COUNT(*)
                   FROM FINAL_TABLE
                   WHERE Preferred = 1''')
    data = cur.fetchall()
    for row in data:
        print(row)
    return


def write_result_to_file(c):
    cursor = c.cursor()
    cursor.execute("SELECT * FROM FINAL_TABLE")
    rows = cursor.fetchall()
    with open("test1.tsv", "w", newline="", encoding='utf-8') as f:  # On Python 3.x use "w" mode and newline=""
        writer = csv.writer(f, delimiter="|")  # create a CSV writer, tab delimited
        writer.writerows(rows)  # write your SQLite data
    return


