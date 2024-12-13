import xlrd

# 指定 .xls 文件路徑
file_path = "static/課程查詢_1131130204122.xls"

import xlrd  # 假設用的是 xlrd 讀取 Excel 表格
from datetime import datetime

# 定義表格中每一欄的預期型別
EXPECTED_TYPES = {
    0: int,  # id
    1: str,  # semester
    2: str,  # primary_instructor
    3: str,  # course_code_new
    4: str,  # department_code
    5: str,  # core_code
    6: str,  # course_group
    7: str,  # grade
    8: str,  # class_group
    9: str,  # course_name_cn
    10: str,  # course_name_en
    11: str,  # instructor_name
    12: int,  # enrollment
    13: int,  # male_students
    14: int,  # female_students
    15: int,  # credits
    16: str,  # weeks
    17: float,  # hours_per_week
    18: str,  # course_type_code
    19: str,  # course_type
    20: str,  # location
    21: str,  # weekday
    22: str,  # class_period
    23: str,  # notes
    24: str,  # course_summary_cn
    25: str,  # course_summary_en
    26: str,  # primary_instructor_code_old
    27: str,  # course_code_old
    28: str,  # schedule_code_old
    29: str,  # schedule_name_old
    30: str,  # instructor_code_old
    31: str,  # course_class
}

def check_cell_type(cell_value, expected_type):
    """檢查單元格值是否符合預期型別"""
    if expected_type == int:
        return isinstance(cell_value, (int, float)) and cell_value == int(cell_value)
    elif expected_type == float:
        return isinstance(cell_value, (int, float))
    elif expected_type == str:
        return isinstance(cell_value, str)
    else:
        return False

try:
    # 打開 Excel 文件
    workbook = xlrd.open_workbook("static/課程查詢_1131130204122.xls")
    sheet = workbook.sheet_by_index(0)

    # 遍歷所有的行與列
    for row_index in range(6, sheet.nrows):  # 假設第一行是標題行
        for col_index in range(sheet.ncols):
            try:
                cell_value = sheet.cell_value(row_index, col_index)
                expected_type = EXPECTED_TYPES.get(col_index)

                # 如果有定義型別，檢查型別是否正確
                if expected_type and not check_cell_type(cell_value, expected_type):
                    print(f"型別錯誤 - Row: {row_index + 1}, Column: {col_index + 1}, "
                          f"Value: {cell_value}, Expected Type: {expected_type.__name__}")
            except Exception as cell_error:
                print(f"讀取錯誤 - Row: {row_index + 1}, Column: {col_index + 1}: {cell_error}")

except Exception as e:
    print(f"讀取檔案錯誤: {e}")
