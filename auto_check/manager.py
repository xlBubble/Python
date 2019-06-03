# -*- coding: utf-8 -*-
import txy
import aliy
import json
import xlrd
from xlutils.copy import copy

def update_csv(data):
    # 写入csv文件
    # csv 头部：'异地登录', '暴力破解', '木马文件', '安全基线', '漏洞风险', '7天内过期'
    # 读取csv行数
    file = xlrd.open_workbook('info.csv')
    file_sheet = file.sheet_by_index(0)
    row_num = file_sheet.nrows
    print(row_num)
    # 写入csv
    myWorkBook = copy(file)
    sheet = myWorkBook.get_sheet(0)
    col = 0
    # row_num += 1
    for cell in data:
        sheet.write(row_num, col, cell)
        col += 1
    myWorkBook.save('info.csv')
    return 0

def main():
    with open("info.json", 'r') as f:
        get_info = json.load(f)
    for item in get_info["info"]:
        if item["type"] == "txy":
            monitor = txy.get_main(item)
            data = [monitor["NonlocalLoginNum"], monitor["BruteAttackSuccessNum"], monitor['VulNum'],
                    monitor['BaseLineNum'], monitor['MalwareNum'], monitor['dead_in_7d']]
            data.insert(0, item['name'])
            print(data)
            update_csv(data)
        if item["type"] == "aliy":
            #monitor = aliy.get_main(item)
            pass

    return 0

if __name__ == '__main__':
    main()

