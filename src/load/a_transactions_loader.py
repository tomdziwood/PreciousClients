import codecs


class ATransaction:
    def __init__(self, transid, transtype, transdate, custid, prodid, quantity, price, discount, returnid, reason):
        self.transid = transid
        self.transtype = transtype
        self.transdate = transdate
        self.custid = custid
        self.prodid = prodid
        self.quantity = quantity
        self.price = price
        self.discount = discount
        self.returnid = returnid
        self.reason = reason

    def __str__(self):
        str_list = [str(self.transid),
                    self.transtype,
                    self.transdate,
                    str(self.custid),
                    self.prodid if (self.prodid is not None) else "None",
                    str(self.quantity) if (self.quantity is not None) else "None",
                    str(self.price),
                    str(self.discount) if (self.discount is not None) else "None",
                    str(self.returnid) if (self.returnid is not None) else "None",
                    self.reason if (self.reason is not None) else "None"]

        return '|'.join(str_list)


def read_a_transactions():
    a_transaction_list = []

    with codecs.open('../../data/a-transactions.dat', encoding='iso-8859-1') as file:
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


def main():
    a_transaction_list = read_a_transactions()
    print(str(len(a_transaction_list)))
    [print(x) for x in a_transaction_list[:30]]


if __name__ == '__main__':
    main()
