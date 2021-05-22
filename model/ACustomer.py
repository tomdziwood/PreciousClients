class ACustomer:
    def __init__(self, custid, fname, lname, street_address, district, voivodship, postcode, preferred):
        self.custid = custid
        self.fname = fname
        self.lname = lname
        self.street_address = street_address
        self.district = district
        self.voivodship = voivodship
        self.postcode = postcode
        self.preferred = preferred

    def __str__(self):
        str_list = [str(self.custid),
                    self.fname,
                    self.lname,
                    self.street_address,
                    self.district,
                    self.voivodship,
                    str(self.postcode),
                    str(self.preferred)]

        return '|'.join(str_list)
