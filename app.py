import codecs
import sqlite3

from model.ACustomer import ACustomer
from model.ATransaction import ATransaction
from model.BCustomer import BCustomer
from model.BTransaction import BTransaction
from model.CustInfo import CustInfo
from database import create_tables, create_connection, insert_data_into_table, test_join


def read_a_customers():
    a_customer_list = []

    with codecs.open('data/a-customers.dat', encoding='iso-8859-2') as file:
        for line in file:
            custid = int(line[:8])
            fname = line[8:28].rstrip()
            lname = line[28:53].rstrip()
            street_address = line[53:143].rstrip()
            district = line[143:173].rstrip()
            voivodship = line[173:193].rstrip()
            postcode = int(line[193:198])
            preferred = True if '1' == line[198] else False

            a_customer = ACustomer(custid, fname, lname, street_address, district, voivodship, postcode, preferred)
            # print(a_customer)

            a_customer_list.append(a_customer)

    return a_customer_list


def read_a_transactions():
    a_transaction_list = []

    with codecs.open('data/a-transactions.dat', encoding='iso-8859-1') as file:
        for line in file:
            transid = int(line[:9])
            transtype = line[9:12].rstrip()
            transdate = line[12:18].rstrip()
            custid = int(line[18:26])
            prodid = line[26:34] if transtype == 'PUR' else None
            quantity = int(line[34:37]) if transtype == 'PUR' else None
            price = int(line[37:43])
            discount = int(line[43:45]) if transtype == 'PUR' else None
            returnid = int(line[45:54]) if transtype == 'RET' else None
            reason = line[54:84] if transtype == 'RET' else None

            a_transaction = ATransaction(transid, transtype, transdate, custid, prodid, quantity, price, discount,
                                         returnid, reason)
            # print(a_transaction)

            a_transaction_list.append(a_transaction)

    return a_transaction_list


def read_b_customers():
    b_customer_list = []

    with codecs.open('data/b-customers.dat', encoding='windows-1250') as file:
        for line in file:
            splitted = line.split(sep="|")

            custid = int(splitted[0])
            firstname = splitted[1]
            lastname = splitted[2]
            street_address = splitted[3]
            district = splitted[4]
            voivodship = splitted[5]
            postcode = int(splitted[6][:2]) * 1000 + int(splitted[6][3:6])

            b_customer = BCustomer(custid, firstname, lastname, street_address, district, voivodship, postcode)
            # print(b_customer)

            b_customer_list.append(b_customer)

    return b_customer_list


def read_b_transactions():
    b_transaction_list = []

    with codecs.open('data/b-transactions.dat', encoding='iso-8859-1') as file:
        for line in file:
            splitted = line.split(sep=",")

            transid = int(splitted[0])
            prodid = splitted[1]
            price = int(splitted[2])
            quantity = int(splitted[3])
            transdate = splitted[4]
            custid = int(splitted[0])

            b_transaction = BTransaction(transid, prodid, price, quantity, transdate, custid)
            # print(b_transaction)

            b_transaction_list.append(b_transaction)

    return b_transaction_list


def read_cust_info():
    cust_info_list = []

    with codecs.open('data/cust-info.dat', encoding='IBM037') as file:
        fileInOneLine = file.readline()
        n = 307
        for i in range(0, len(fileInOneLine), n):
            line = fileInOneLine[i:i+n]

            id = int(line[:9])
            firstname = line[9:51].rstrip()
            lastname = line[51:83].rstrip()
            street_address = line[83:193].rstrip()
            district = line[193:233].rstrip()
            voivodship = line[233:283].rstrip()
            postcode = int(line[283:288])
            est_income = int(line[288:296])
            own_or_rent = line[296]
            date = line[297:307]

            cust_info = CustInfo(id, firstname, lastname, street_address, district, voivodship, postcode, est_income, own_or_rent, date)
            # print(cust_info)

            cust_info_list.append(cust_info)

    return cust_info_list


def main():
    a_customer_list = read_a_customers()
    a_transaction_list = read_a_transactions()
    b_customer_list = read_b_customers()
    b_transaction_list = read_b_transactions()
    cust_info_list = read_cust_info()

    # ostatni = cust_info_list[-1]
    # print(ostatni)
    # street_address: str = ostatni.street_address
    # print(street_address)
    # print(street_address.encode(encoding='utf-8'))
    # print(street_address.encode(encoding='iso-8859-2'))
    #print(b_customer_list[0].firstname)

    '''Moje'''
    conn = create_connection('test.db')
    # create_tables(conn)
    # insert_data_into_table(a_customer_list, 'A_CUSTOMERS', conn)
    # insert_data_into_table(a_transaction_list, 'A_TRANSACTIONS', conn)
    # insert_data_into_table(b_customer_list, 'B_CUSTOMERS', conn)
    # insert_data_into_table(b_transaction_list, 'B_TRANSACTIONS', conn)
    test_join(conn)


if __name__ == '__main__':
    main()
