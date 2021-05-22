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
