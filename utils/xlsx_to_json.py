# Import openyxl module
import openpyxl
import os
import json
title = "Text_JPN_1.4.xlsx"
out = "./Text_JPN_1.4_out/"
# Define variable to load the wookbook
wb = openpyxl.load_workbook(title)
try:
    os.mkdir(out)
except FileExistsError:
    pass
# Define variable to read the active sheet:
# worksheet = wb.active
# print(wb.get_sheet_names())
for sheet_name in wb.get_sheet_names():
    sheet = wb.get_sheet_by_name(sheet_name)
    out_json = {}
    all_rows = sheet.rows
    for row in all_rows:
        idx = row[0].value
        msg = row[1].value
        label = row[2].value
        text = row[3].value
        if idx is None:
            break
        out_json[label] = text
        # print(label, text)
    with open(out + sheet_name + ".json", "w", encoding="utf-8") as f:
        f.write(json.dumps(out_json, indent=4 ,ensure_ascii=False))
        # print('')
    # input()