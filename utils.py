import csv

def write_to_csv(row):
    # open the file in the write mode
    with open('test.csv', 'w') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(row)

if __name__ == "__main__":
    header = ['name', 'area', 'country_code2', 'country_code3']
    data = ['Afghanistan', 652090, 'AF', 'AFG']
    write_to_csv()