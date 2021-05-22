class BCustomer:
    def __init__(self, custid, firstname, lastname, street_address, district, voivodship, postcode):
        self.custid = custid
        self.firstname = firstname
        self.lastname = lastname
        self.street_address = street_address
        self.district = district
        self.voivodship = voivodship
        self.postcode = postcode

    def __str__(self):
        str_list = [str(self.custid),
                    self.firstname,
                    self.lastname,
                    self.street_address,
                    self.district,
                    self.voivodship,
                    str(self.postcode)]

        return '|'.join(str_list)
