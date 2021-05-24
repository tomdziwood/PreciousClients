import codecs


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


def converse_words_with_native_characters(string: str):
    return bytes(string, encoding='raw_unicode_escape').decode(encoding='iso-8859-2')


def read_cust_info():
    cust_info_list = []

    with codecs.open('../../data/cust-info.dat', encoding='IBM037') as file:
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


def main():
    cust_info_list = read_cust_info()
    print(str(len(cust_info_list)))
    [print(x) for x in cust_info_list[:30]]


if __name__ == '__main__':
    main()
