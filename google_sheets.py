import gspread


class GoogleSheets:

    def __init__(self, row_lst):
        self.row_lst = row_lst
        self.insert_to_sheets()

    def insert_to_sheets(self):

        try:
            print(self.row_lst)
            service_account = gspread.service_account(filename='striped-harbor-395519-a1c31e3d285a.json')
            sheet = service_account.open('Headers')
            worksheet = sheet.worksheet('Sheet2')
            print("------ Inserting into Excel ------")
            print('Row count: ', worksheet.row_count)
            print('Col count: ', worksheet.col_count)
            worksheet.append_row(self.row_lst)

            return True

        except Exception as e:
            return e

if __name__ == "__main__":
    x = GoogleSheets(['11/08/2023 11:42:38', 'XYZ', '0', '0', '100', 'Guest post (2)', 'Draft', '0', '0', '0 ', '0 ', '0', '0', '0', '0', '0', '0', '0', '0'])