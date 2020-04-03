import openpyxl
import re
from lcoConfig import output_file, output_column, can_column, stb_column, max_rows

def getDict():
    can_dict = {}
    stb_dict = {}

    wb = openpyxl.load_workbook(output_file)
    sheet = wb.active
    pattern1 = r'CAN\d+'
    pattern2 = r'\d+'
    index = 1
    for c1,c2 in sheet.iter_rows(min_row=1, min_col=1, max_row = max_rows, max_col = 2):
        s1 = str(c1.value).strip()
        s2 = str(c2.value).strip()
        if re.search(pattern1, s1):
            can_dict[s1] = index
        if re.search(pattern2, s2):
            stb_dict[s2] = index
        index=index+1

    return can_dict, stb_dict
        