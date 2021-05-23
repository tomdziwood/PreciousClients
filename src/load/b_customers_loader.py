import codecs


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


def read_b_customers():
    b_customer_list = []

    with codecs.open('../../data/b-customers.dat', encoding='windows-1250') as file:
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


def main():
    b_customer_list = read_b_customers()
    print(str(len(b_customer_list)))
    [print(x) for x in b_customer_list[:30]]


if __name__ == '__main__':
    main()
