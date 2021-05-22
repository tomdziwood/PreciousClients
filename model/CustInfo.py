class CustInfo:
    def __init__(self, id, firstname, lastname, street_address, district, voivodship, postcode, est_income, own_or_rent, date):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.street_address = street_address
        self.district = district
        self.voivodship = voivodship
        self.postcode = postcode
        self.est_income = est_income
        self.own_or_rent = own_or_rent
        self.date = date

    def __str__(self):
        str_list = [str(self.id),
                    self.firstname,
                    self.lastname,
                    self.street_address,
                    self.district,
                    self.voivodship,
                    str(self.postcode),
                    str(self.est_income),
                    self.own_or_rent,
                    self.date]

        return '|'.join(str_list)
