import codecs


class BTransaction:
    def __init__(self, transid, prodid, price, quantity, transdate, custid):
        self.transid = transid
        self.prodid = prodid
        self.price = price
        self.quantity = quantity
        self.transdate = transdate
        self.custid = custid

    def __str__(self):
        str_list = [str(self.transid),
                    self.prodid,
                    str(self.price),
                    str(self.quantity),
                    self.transdate,
                    str(self.custid)]

        return '|'.join(str_list)


def read_b_transactions():
    b_transaction_list = []

    with codecs.open('../../data/b-transactions.dat', encoding='iso-8859-1') as file:
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


def main():
    b_transaction_list = read_b_transactions()
    print(str(len(b_transaction_list)))
    [print(x) for x in b_transaction_list[:30]]


if __name__ == '__main__':
    main()
