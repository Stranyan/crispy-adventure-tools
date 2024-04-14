import json
import os
import csv
import re

def get_output():
    # 设置
    # filepath = r"C:\Users\winor\Desktop\Files\丽香\小中甸\20240315-backup" # 指定路径和文件后缀
    filepath = r""
    extension = ".backup" # 指定文件后缀
    stopnum = 100 # 设置要在多少号的预置位停止，以防止热成像球机预置位重复
    # output_file_name = "output.txt"  # 设置输出文件名
    output_csv_name = "output.csv"  # 设置输出 CSV 文件路径
    ip_head = "198.1.2."

    # output_file_path = os.path.join(filepath, output_file_name)
    output_csv_path = os.path.join(filepath, output_csv_name)

    # 打开输出文件
    # with open(output_file_path, 'w', encoding='utf-8') as output_file:
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # 写入 CSV 文件的表头
        csv_writer.writerow(['IP', 'PresetID', 'Name'])
        # 获取指定路径下所有文件
        files = os.listdir(filepath)

        # 筛选后缀为 .backup 的文件名
        backup_files = [file for file in files if file.endswith(extension)]

        # 打印结果
        for backup_file in backup_files:
            # 使用 UTF-8 或者 GB-2312 编码打开 JSON 文件
            filename = str(backup_file)

            if "hw" not in filename: 
                with open(os.path.join(filepath, filename), 'r', encoding='utf-8') as file:
                    data = json.load(file)
            else:
                with open(os.path.join(filepath, filename), 'r', encoding='gb2312') as file:
                    data = json.load(file)

            # 获取 "Name" 字段的值
            countnum = 1
            ip_match = re.search(r'\d+', backup_file)  # 使用正则表达式提取数字部分
            ip_last = ip_match.group() if ip_match else backup_file
            ip = ip_head + ip_last
            for preset_group in data["PtzPreset"]:
                presetid = 0
                for preset in preset_group:
                    countnum += 1
                    presetid += 1
                    if preset.get("Enable") == True:
                        name_value = preset.get("Name")
                        if name_value is not None and name_value != "守望位":
                            # print(name_value)
                            # output_file.write(name_value + '\n')
                            csv_writer.writerow([ip, presetid, name_value]) # 将结果写入文件

                    # 当 countnum 等于 stopnum 时，停止循环
                    if countnum == stopnum:
                        break

                # 在外部循环中再次检查 countnum 是否等于 stopnum，如果是，终止外部循环
                if countnum == stopnum:
                    break

        print("Done!")