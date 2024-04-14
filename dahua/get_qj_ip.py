import xlrd

def get_qj_info(workbook_url=r'C:\Users\winor\Documents\我的数据库-20240319.xlsx', sheet_num=0):
    # workbook = xlrd.open_workbook(r'C:\Users\winor\Documents\我的数据库-20240319.xlsx')
    # sheet = workbook.sheet_by_index(0)

    # 打开 Excel 文件
    workbook = xlrd.open_workbook(f'{workbook_url}')

    # 选择第一个工作表
    sheet = workbook.sheet_by_index(sheet_num)
    
    # 创建一个空字典来存储结果
    device_dict = {}

    # 遍历每一行，将设备名称作为键，设备子类和 IP 地址作为值添加到字典中
    for row in range(1, sheet.nrows):  # 从第二行开始遍历，因为第一行是标题
        device_name = sheet.cell_value(row, 2)  # 设备名称所在的列为第三列，索引为2
        device_subtype = sheet.cell_value(row, 1)  # 设备子类所在的列为第二列，索引为1
        ip = sheet.cell_value(row, 3)  # IP 所在的列为第四列，索引为3
        device_dict[device_name] = {'device_subtype': device_subtype, 'ip': ip}

    # 打印符合条件的设备信息
    # print("符合条件的设备信息:")
    device_qj_dict = {}
    for device_name, info in device_dict.items():
        chno = "0"
        if info['device_subtype'] in ["球机", "热成像球机", "半球机", "云台", "云台枪机"]:
            if "热成像球机B" in device_name:
                chno = "1"
                # print(f"设备名称: {device_name}, 设备子类: {info['device_subtype']}, IP: {info['ip']}, chno: {chno}")
            # else:
                # print(f"设备名称: {device_name}, 设备子类: {info['device_subtype']}, IP: {info['ip']}, chno: {chno}")
            device_qj_dict[device_name] = {'device_subtype': info['device_subtype'], 'ip': info['ip'], 'chno': chno}
    # print(device_qj_dict)
    return device_qj_dict

# workbook_url = r'C:\Users\winor\Documents\我的数据库-20240319.xlsx'
# sheet_num = 0
# get_qj_info(workbook_url, sheet_num)
# get_qj_info()