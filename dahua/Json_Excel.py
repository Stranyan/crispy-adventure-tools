import json
import os
import csv
import re
import datetime

def get_output(filepath="backup/", extension=".backup", startnum=300, stopnum=100, ip_head="198.1.2."):
    # 获取当前时间
    current_time = datetime.datetime.now()
    
    # 格式化当前时间字符串
    time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    output_csv_name = f"output_{time_str}.csv"
    output_csv_path = os.path.join(filepath, output_csv_name)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['IP', 'PresetID', 'Name'])

        files = os.listdir(filepath)
        backup_files = [file for file in files if file.endswith(extension)]

        for backup_file in backup_files:
            enabled_names = []
            filename = os.path.join(filepath, backup_file)
            ip_match = re.search(r'\d+', backup_file)
            ip_last = ip_match.group() if ip_match else backup_file
            ip = ip_head + ip_last
            presetid = 0

            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)

            countnum = 1
            for preset_group in data["params"][0]["params"]["table"][0]:
                countnum += 1
                if preset_group["Enable"]:
                    enabled_names.append(preset_group["Name"])
                    if countnum == stopnum:
                        break

            for name_value in enabled_names:
                if name_value is not None and name_value.strip() != "" and name_value != "守望位":
                    # print(name_value)
                    presetid += 1
                    csv_writer.writerow([ip, presetid, name_value])

    print(f"Done! 保存为{output_csv_name}")

get_output()
