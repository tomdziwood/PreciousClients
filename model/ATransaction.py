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
