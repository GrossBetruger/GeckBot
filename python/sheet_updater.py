import os
from typing import List

import gspread
import pandas as pd
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials

COLUMNS_FORMATTING = CellFormat(
    backgroundColor=Color.fromHex("#7733FF"),
    textFormat=TextFormat(bold=True, foregroundColor=Color.fromHex("#FFFFFF")),
    horizontalAlignment='CENTER'
    )

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
    format_cell_range(worksheet, 'A1:F1', COLUMNS_FORMATTING)
    worksheet.update(data)


if __name__ == '__main__':
    data = pd.DataFrame([['data1', 'data2'], ['data3', 'data4']], columns=['col1', 'col2'])
    update_sheet("test sheet", data)
    print(read_sheet("test sheet"))
