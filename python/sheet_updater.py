import os
import gspread

from typing import Union, List
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd



scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.expanduser('~/.geckobot.json'),
                                                         scope)
client = gspread.authorize(creds)


def get_sheet_id_by_title(gspread_client: gspread.client.Client, title: str):
    for sheet in gspread_client.openall():
        if sheet.title == title:
            return sheet.id
    raise Exception(f"sheet not found: {title}")


def read_sheet(title: str) -> List[tuple]:
    global client
    sheet = client.open(title).sheet1
    return sheet.get_all_records()


def update_sheet(spreadsheet_title: str, data: pd.DataFrame):
    global client
    data = [data.columns.values.tolist()] + data.values.tolist()
    worksheet = client.open(spreadsheet_title).sheet1
    worksheet.update(data)


if __name__ == '__main__':
    data = pd.DataFrame([['data1', 'data2'], ['data3', 'data4']], columns=['col1', 'col2'])
    update_sheet("test sheet", data)
    print(read_sheet("test sheet"))

