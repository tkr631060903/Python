#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import os

sys.path.append(os.path.realpath("."))
import numpy as np
import pandas as pd
import openpyxl
from openpyxl import load_workbook

# df=pd.DataFrame()
# # df.to_excel("test.xlsx",sheet_name="sheet1")
# data=pd.read_excel("test.xlsx", "sheet1", index_col=None, na_values=["NA"])
# print(df)
# print(data)
wb=load_workbook("test.xlsx")
sh=wb.active
print(sh)
sh['A2'] = 2
wb.save('test.xlsx')