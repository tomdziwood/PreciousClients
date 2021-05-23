import codecs
import sqlite3

from model.ACustomer import ACustomer
from model.ATransaction import ATransaction
from model.BCustomer import BCustomer
from model.BTransaction import BTransaction
from model.CustInfo import CustInfo
from database import create_tables, create_connection, insert_data_into_table, test_join, calculate_b_transactions


def read_a_customers():
    a_customer_list = []

    with codecs.open('data/a-customers.dat', encoding='iso-8859-2') as file:
        for line in file:
            custid = int(line[:8])
            fname = line[8:28].rstrip().upper()
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

            a_transaction = ATransaction(transid, transtype, transdate, custid, prodid, quantity, price, discount, returnid, reason)
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
            voivodship = splitted[5].upper()
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
            custid = int(splitted[5])

            b_transaction = BTransaction(transid, prodid, price, quantity, transdate, custid)
            # print(b_transaction)

            b_transaction_list.append(b_transaction)

    return b_transaction_list


NATIVE_POLISH_IBM = ['¯', 'Æ', '¿', '¼', 'æ', '³', '¦', 'ñ', '¶', '£', '±', 'ê', '^']
NATIVE_POLISH_ISO = ['Ż', 'Ć', 'ż', 'ź', 'ć', 'ł', 'Ś', 'ń', 'ś', 'Ł', 'ą', 'ę', 'Ź']


def converse_native_characters(character: str):
    if character in NATIVE_POLISH_IBM:
        i = NATIVE_POLISH_IBM.index(character)
        return NATIVE_POLISH_ISO[i].encode(encoding="iso-8859-2")
    else:
        return character.encode(encoding="iso-8859-2")


def converse_words_with_native_characters(string: str):
    list_of_bytes = [converse_native_characters(character) for character in string]
    concatenated_bytes = b''.join(list_of_bytes)
    new_string = codecs.decode(concatenated_bytes, encoding='iso-8859-2')
    return new_string


def read_cust_info():
    cust_info_list = []

    with codecs.open('data/cust-info.dat', encoding='IBM037') as file:
        fileInOneLine = file.readline()
        n = 307
        for i in range(0, len(fileInOneLine), n):
            line = fileInOneLine[i:i + n]

            id = int(line[:9])
            firstname = converse_words_with_native_characters(line[9:51].rstrip())
            lastname = converse_words_with_native_characters(line[51:83].rstrip()).upper()
            street_address = converse_words_with_native_characters(line[83:193].rstrip())
            district = converse_words_with_native_characters(line[193:233].rstrip())
            voivodship = converse_words_with_native_characters(line[233:283].rstrip()).upper()
            postcode = int(line[283:288])
            est_income = int(line[288:296])
            own_or_rent = line[296]
            date = line[297:307]

            cust_info = CustInfo(id, firstname, lastname, street_address, district, voivodship, postcode, est_income, own_or_rent, date)
            # print(cust_info)

            cust_info_list.append(cust_info)

    return cust_info_list


def check_all_characters(cust_info_list):
    all_distinct_letters = set()
    for cust_info in cust_info_list:
        # print(str(cust_info))
        distinct_letters = set(str(cust_info))
        # print(distinct_letters)
        all_distinct_letters.update(distinct_letters)

    print(all_distinct_letters)


def check_person_repetition(a_customer_list, b_customer_list, cust_info_list):
    counter = 0
    for a_customer in a_customer_list:
        for b_customer in b_customer_list:
            if (a_customer.fname == b_customer.firstname) and (a_customer.lname.upper() == b_customer.lastname):
                counter += 1
                print("Equal:")
                print(a_customer)
                print(b_customer)
                if a_customer.street_address != b_customer.street_address:
                    print("Different street address!!!")
    print("Counter: " + str(counter))

    counter = 0
    for a_customer in a_customer_list:
        for cust_info in cust_info_list:
            if (a_customer.fname == cust_info.firstname) and (a_customer.lname.upper() == cust_info.lastname.upper()):
                counter += 1
                print("Equal:")
                print(a_customer)
                print(cust_info)
                if a_customer.street_address != cust_info.street_address:
                    print("Different street address!!!")
    print("Counter: " + str(counter))

    counter = 0
    for b_customer in b_customer_list:
        for cust_info in cust_info_list:
            if (b_customer.firstname == cust_info.firstname) and (b_customer.lastname == cust_info.lastname.upper()):
                counter += 1
                print("Equal:")
                print(b_customer)
                print(cust_info)
                if b_customer.street_address != cust_info.street_address:
                    print("Different street address!!!")
    print("Counter: " + str(counter))


def main():
    a_customer_list = read_a_customers()
    print(str(len(a_customer_list)))
    [print(x) for x in a_customer_list[:30]]

    a_transaction_list = read_a_transactions()
    print(str(len(a_transaction_list)))
    [print(x) for x in a_transaction_list[:30]]

    b_customer_list = read_b_customers()
    print(str(len(b_customer_list)))
    [print(x) for x in b_customer_list[:30]]

    b_transaction_list = read_b_transactions()
    print(str(len(b_transaction_list)))
    [print(x) for x in b_transaction_list[:30]]

    cust_info_list = read_cust_info()
    print(str(len(cust_info_list)))
    [print(x) for x in cust_info_list[:30]]

    '''Connect to db'''
    conn = create_connection('test.db')
    '''Uncomment these if you want to initialize your tables and add data to them'''
    # create_tables(conn)
    # insert_data_into_table(a_customer_list, 'A_CUSTOMERS', conn)
    # insert_data_into_table(a_transaction_list, 'A_TRANSACTIONS', conn)
    # insert_data_into_table(b_customer_list, 'B_CUSTOMERS', conn)
    # insert_data_into_table(b_transaction_list, 'B_TRANSACTIONS', conn)
    # insert_data_into_table(cust_info_list, 'C_CUSTOMERINFO', conn)

    # calculate_b_transactions(conn)


if __name__ == '__main__':
    main()
