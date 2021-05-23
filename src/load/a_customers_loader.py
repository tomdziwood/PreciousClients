import codecs


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


def read_a_customers():
    a_customer_list = []

    with codecs.open('../../data/a-customers.dat', encoding='iso-8859-2') as file:
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


def main():
    a_customer_list = read_a_customers()
    print(str(len(a_customer_list)))
    [print(x) for x in a_customer_list[:30]]


if __name__ == '__main__':
    main()
