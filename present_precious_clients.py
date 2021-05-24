import argparse
import csv

from database import create_connection


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--income_threshold', type=int, help='INCOME_THRESHOLD')
    arg_parser.add_argument('--transaction_threshold', type=int, help='TRANSACTION_THRESHOLD')
    arg_parser.add_argument('--vip_income', type=int, help='VIP_INCOME')

    return arg_parser.parse_args()


def main():
    args = parse_args()
    print("Passed parameters:")
    print(args)
    if (args.income_threshold is None) or (args.transaction_threshold is None) or (args.vip_income is None):
        print("Wrong parameters, aborting.")
        return


    '''Connect to db'''
    conn = create_connection('test.db')


    '''Get filtered records from FINAL_TABLE'''
    cur = conn.cursor()
    query = '''SELECT * FROM FINAL_TABLE
               WHERE est_income > ? OR
                    Purchases > ?'''
    parameters = (args.income_threshold, args.transaction_threshold)
    cur.execute(query, parameters)
    result = cur.fetchall()

    all_counter = len(result)
    accepted_counter = 0
    denied_counter = 0
    denied_limit = 200

    with open("output.dat", "w", newline="", encoding='utf-8') as f:  # On Python 3.x use "w" mode and newline=""
        writer = csv.writer(f, delimiter="|")
        for row in result:
            if (row[9] is not None) and (row[9] > args.vip_income) and (denied_counter < denied_limit):
                denied_counter += 1
                # print("VIP_INCOME threshold is blocking")
                continue

            accepted_counter += 1
            # print(row)
            row_formatted = list(row)
            row_formatted[4] = row_formatted[4].ljust(110)
            row_formatted[5] = row_formatted[5].ljust(40)
            row_formatted[6] = row_formatted[6].ljust(50)
            row_formatted[7] = row_formatted[7].rjust(5, '0')
            writer.writerow(row_formatted)

    print("Number of all records:\t\t" + str(all_counter))
    print("Number of denied by VIP_INCOME:\t" + str(denied_counter))
    print("Final number of records:\t" + str(accepted_counter))


'''
example of execution command: 
python present_precious_clients.py --income_threshold=200000 --transaction_threshold=500 --vip_income=10900
'''
if __name__ == '__main__':
    main()